
package com.aiori.ransomwarewarning

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

data class ActivityEvent(
    val timestamp: String,
    val fileId: String,
    val operation: String,
    val fileSize: Long,
    val scenario: String,
    val label: Int
)

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            MaterialTheme {
                RansomwareDashboard(
                    appDirectory = filesDir,
                    onExport = { uri, csv ->
                        contentResolver.openOutputStream(uri)?.use {
                            it.write(csv.toByteArray(Charsets.UTF_8))
                        }
                    }
                )
            }
        }
    }
}

@Composable
fun RansomwareDashboard(
    appDirectory: File,
    onExport: (Uri, String) -> Unit
) {
    val events = remember { mutableStateListOf<ActivityEvent>() }
    val scope = rememberCoroutineScope()

    var simulationJob by remember { mutableStateOf<Job?>(null) }
    var status by remember { mutableStateOf("Ready") }
    var scenario by remember { mutableStateOf("Not started") }
    var normalCount by remember { mutableIntStateOf(0) }
    var suspiciousCount by remember { mutableIntStateOf(0) }

    val isRunning = simulationJob?.isActive == true

    val exportLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.CreateDocument("text/csv")
    ) { uri ->
        if (uri != null) {
            val csv = buildString {
                appendLine(
                    "timestamp,file_id,operation,file_size,scenario_type,label"
                )

                events.forEach { event ->
                    appendLine(
                        "${event.timestamp},${event.fileId}," +
                                "${event.operation},${event.fileSize}," +
                                "${event.scenario},${event.label}"
                    )
                }
            }

            runCatching {
                onExport(uri, csv)
            }.onSuccess {
                status = "CSV exported successfully"
            }.onFailure {
                status = "Export failed: ${it.message}"
            }
        }
    }

    fun recordEvent(
        fileId: String,
        operation: String,
        fileSize: Long,
        scenarioName: String,
        suspicious: Boolean
    ) {
        val timestamp = SimpleDateFormat(
            "yyyy-MM-dd HH:mm:ss.SSS",
            Locale.US
        ).format(Date())

        events.add(
            ActivityEvent(
                timestamp = timestamp,
                fileId = fileId,
                operation = operation,
                fileSize = fileSize,
                scenario = scenarioName,
                label = if (suspicious) 1 else 0
            )
        )

        if (suspicious) {
            suspiciousCount++
        } else {
            normalCount++
        }
    }

    suspend fun runSimulation(
        mode: String,
        suspicious: Boolean,
        fileCount: Int,
        operationsPerFile: Int,
        renameCount: Int,
        deleteCount: Int,
        pauseMillis: Long
    ) {
        val scenarioName = mode
        val folder = File(
            appDirectory,
            "lab_files/${System.currentTimeMillis()}"
        )

        folder.mkdirs()

        var completed = 0

        for (index in 0 until fileCount) {
            val original = File(folder, "lab_file_$index.txt")

            // Operation 1: Create a dummy file
            original.writeText("Controlled laboratory content $index")

            recordEvent(
                original.name,
                "write",
                original.length(),
                scenarioName,
                suspicious
            )
            completed++
            status = "$mode: $completed operations completed"
            delay(pauseMillis)

            // Operation 2: Modify the dummy file
            repeat(operationsPerFile - 1) {
                original.appendText("\nModified test content $index")

                recordEvent(
                    original.name,
                    "modify",
                    original.length(),
                    scenarioName,
                    suspicious
                )
                completed++
                status = "$mode: $completed operations completed"
                delay(pauseMillis)
            }

            // Optional controlled rename
            if (index < renameCount) {
                val renamed = File(
                    folder,
                    "renamed_lab_file_$index.txt"
                )

                if (original.renameTo(renamed)) {
                    recordEvent(
                        renamed.name,
                        "rename",
                        renamed.length(),
                        scenarioName,
                        suspicious
                    )
                    completed++
                    status = "$mode: $completed operations completed"
                    delay(pauseMillis)

                    // Optional controlled deletion
                    if (index < deleteCount && renamed.delete()) {
                        recordEvent(
                            renamed.name,
                            "delete",
                            0L,
                            scenarioName,
                            suspicious
                        )
                        completed++
                        status = "$mode: $completed operations completed"
                        delay(pauseMillis)
                    }
                }
            }
        }

        status = "$mode completed: $completed events recorded"
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Text(
            "Android Ransomware Early Warning",
            style = MaterialTheme.typography.headlineSmall
        )

        Spacer(modifier = Modifier.height(6.dp))

        Text(
            "Controlled laboratory behavior monitoring",
            style = MaterialTheme.typography.bodyMedium
        )

        Spacer(modifier = Modifier.height(12.dp))

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(14.dp)) {
                Text("Monitoring Status")
                Spacer(modifier = Modifier.height(5.dp))

                Text(
                    status,
                    style = MaterialTheme.typography.titleMedium
                )

                Text("Scenario: $scenario")
            }
        }

        Spacer(modifier = Modifier.height(10.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Card(modifier = Modifier.weight(1f)) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text("Normal events")
                    Text(
                        "$normalCount",
                        style = MaterialTheme.typography.headlineMedium
                    )
                }
            }

            Card(modifier = Modifier.weight(1f)) {
                Column(modifier = Modifier.padding(12.dp)) {
                    Text("Suspicious events")
                    Text(
                        "$suspiciousCount",
                        style = MaterialTheme.typography.headlineMedium
                    )
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        Text(
            "Simulation Controls",
            style = MaterialTheme.typography.titleMedium
        )

        Spacer(modifier = Modifier.height(6.dp))

        Button(
            onClick = {
                scenario = "Normal activity"
                status = "Starting normal simulation"

                simulationJob = scope.launch {
                    runSimulation(
                        mode = "normal_activity",
                        suspicious = false,
                        fileCount = 40,
                        operationsPerFile = 2,
                        renameCount = 0,
                        deleteCount = 0,
                        pauseMillis = 150
                    )
                }
            },
            enabled = !isRunning,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Start Normal Activity")
        }

        Spacer(modifier = Modifier.height(6.dp))

        Button(
            onClick = {
                scenario = "Moderate ransomware-like activity"
                status = "Starting moderate simulation"

                simulationJob = scope.launch {
                    runSimulation(
                        mode = "moderate_suspicious",
                        suspicious = true,
                        fileCount = 40,
                        operationsPerFile = 2,
                        renameCount = 10,
                        deleteCount = 5,
                        pauseMillis = 150
                    )
                }
            },
            enabled = !isRunning,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Start Moderate Simulation")
        }

        Spacer(modifier = Modifier.height(6.dp))

        Button(
            onClick = {
                scenario = "High-intensity ransomware-like activity"
                status = "Starting high-intensity simulation"

                simulationJob = scope.launch {
                    runSimulation(
                        mode = "high_intensity_suspicious",
                        suspicious = true,
                        fileCount = 60,
                        operationsPerFile = 3,
                        renameCount = 60,
                        deleteCount = 30,
                        pauseMillis = 100
                    )
                }
            },
            enabled = !isRunning,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Start High-Intensity Simulation")
        }

        Spacer(modifier = Modifier.height(6.dp))

        OutlinedButton(
            onClick = {
                simulationJob?.cancel()
                simulationJob = null
                status = "Simulation stopped"
            },
            enabled = isRunning,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Stop Simulation")
        }

        OutlinedButton(
            onClick = {
                exportLauncher.launch("android_activity_events.csv")
            },
            enabled = events.isNotEmpty(),
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Export Events as CSV")
        }

        Spacer(modifier = Modifier.height(10.dp))

        Text(
            "Activity Event Log",
            style = MaterialTheme.typography.titleMedium
        )

        Spacer(modifier = Modifier.height(5.dp))

        LazyColumn(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(5.dp)
        ) {
            items(events.reversed()) { event ->
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(9.dp)) {
                        Text("File: ${event.fileId}")
                        Text("Operation: ${event.operation}")
                        Text("Size: ${event.fileSize} bytes")
                        Text(
                            if (event.label == 1)
                                "Label: Suspicious"
                            else
                                "Label: Benign"
                        )
                        Text(
                            "Scenario: ${event.scenario}",
                            style = MaterialTheme.typography.bodySmall
                        )
                        Text(
                            event.timestamp,
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                }
            }
        }

        Text(
            "Lab prototype: operations are restricted to this app's private storage.",
            style = MaterialTheme.typography.bodySmall
        )
    }
}
