package com.aiori.ransomwarewarning

import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch
import java.io.File

class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            MaterialTheme(
                colorScheme = lightColorScheme(
                    primary = Color(0xFF0284C7),
                    onPrimary = Color.White,
                    primaryContainer = Color(0xFFE0F2FE),
                    onPrimaryContainer = Color(0xFF0369A1),
                    background = Color(0xFFF8FAFC),
                    surface = Color.White,
                    surfaceVariant = Color(0xFFF1F5F9),
                    outline = Color(0xFFCBD5E1)
                )
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    AndroidRansomwareLabApp(
                        appDirectory = filesDir,
                        onExport = { uri, csvContent ->
                            contentResolver.openOutputStream(uri)?.use { stream ->
                                stream.write(csvContent.toByteArray(Charsets.UTF_8))
                            }
                        }
                    )
                }
            }
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AndroidRansomwareLabApp(
    appDirectory: File,
    onExport: (Uri, String) -> Unit
) {
    val engine = remember { SimulationEngine(appDirectory) }
    val scope = rememberCoroutineScope()

    var selectedTab by remember { mutableIntStateOf(0) }
    var currentJob by remember { mutableStateOf<Job?>(null) }
    var statusMessage by remember { mutableStateOf("System Ready. Select a scenario to begin.") }
    var activeScenarioName by remember { mutableStateOf("None") }

    val isRunning = currentJob?.isActive == true

    // File export launcher
    val exportLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.CreateDocument("text/csv")
    ) { uri ->
        if (uri != null) {
            runCatching {
                val csv = engine.exportToCsvString()
                onExport(uri, csv)
            }.onSuccess {
                statusMessage = "Exported ${engine.events.size} events to CSV."
            }.onFailure { err ->
                statusMessage = "Export failed: ${err.localizedMessage}"
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text(
                            "Cipher Aegis Lab Monitor",
                            fontWeight = FontWeight.Bold,
                            fontSize = 18.sp
                        )
                        Text(
                            "AIORI PS-001 | Ransomware Early Warning",
                            fontSize = 12.sp,
                            color = Color(0xFF64748B)
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White
                )
            )
        },
        bottomBar = {
            NavigationBar(containerColor = Color.White) {
                NavigationBarItem(
                    selected = selectedTab == 0,
                    onClick = { selectedTab = 0 },
                    icon = { Text("🧪", fontSize = 18.sp) },
                    label = { Text("Simulation") }
                )
                NavigationBarItem(
                    selected = selectedTab == 1,
                    onClick = { selectedTab = 1 },
                    icon = { Text("🛡️", fontSize = 18.sp) },
                    label = { Text("Diagnostics") }
                )
                NavigationBarItem(
                    selected = selectedTab == 2,
                    onClick = { selectedTab = 2 },
                    icon = { Text("ℹ️", fontSize = 18.sp) },
                    label = { Text("About") }
                )
            }
        }
    ) { paddingValues ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            when (selectedTab) {
                0 -> SimulationLabScreen(
                    engine = engine,
                    isRunning = isRunning,
                    statusMessage = statusMessage,
                    activeScenarioName = activeScenarioName,
                    onStartNormal = {
                        activeScenarioName = "Normal Activity"
                        statusMessage = "Running Normal Activity simulation..."
                        currentJob = scope.launch {
                            engine.runNormalSimulation { msg, _ -> statusMessage = msg }
                            statusMessage = "Normal simulation completed."
                        }
                    },
                    onStartModerate = {
                        activeScenarioName = "Moderate Suspicious"
                        statusMessage = "Running Moderate Suspicious simulation..."
                        currentJob = scope.launch {
                            engine.runModerateSimulation { msg, _ -> statusMessage = msg }
                            statusMessage = "Moderate simulation completed."
                        }
                    },
                    onStartHighIntensity = {
                        activeScenarioName = "High-Intensity Suspicious"
                        statusMessage = "Running High-Intensity simulation..."
                        currentJob = scope.launch {
                            engine.runHighIntensitySimulation { msg, _ -> statusMessage = msg }
                            statusMessage = "High-Intensity simulation completed."
                        }
                    },
                    onStop = {
                        currentJob?.cancel()
                        currentJob = null
                        statusMessage = "Simulation stopped by user."
                    },
                    onReset = {
                        currentJob?.cancel()
                        currentJob = null
                        engine.reset()
                        activeScenarioName = "None"
                        statusMessage = "Lab storage reset. Ready."
                    },
                    onExportCsv = {
                        exportLauncher.launch("android_simulation_events.csv")
                    }
                )

                1 -> DiagnosticsScreen(engine = engine)

                2 -> AboutScopeScreen()
            }
        }
    }
}

@Composable
fun SimulationLabScreen(
    engine: SimulationEngine,
    isRunning: Boolean,
    statusMessage: String,
    activeScenarioName: String,
    onStartNormal: () -> Unit,
    onStartModerate: () -> Unit,
    onStartHighIntensity: () -> Unit,
    onStop: () -> Unit,
    onReset: () -> Unit,
    onExportCsv: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Status Card
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            shape = RoundedCornerShape(12.dp)
        ) {
            Column(modifier = Modifier.padding(14.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        "Status: ${if (isRunning) "ACTIVE" else "IDLE"}",
                        fontWeight = FontWeight.Bold,
                        color = if (isRunning) Color(0xFF0284C7) else Color(0xFF475569)
                    )
                    Text(
                        "Scenario: $activeScenarioName",
                        fontSize = 12.sp,
                        color = Color(0xFF64748B)
                    )
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    statusMessage,
                    fontSize = 13.sp,
                    color = Color(0xFF334155)
                )
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        // Action Buttons Grid
        Text(
            "Controlled Lab Scenarios",
            fontWeight = FontWeight.SemiBold,
            fontSize = 14.sp,
            color = Color(0xFF1E293B)
        )
        Spacer(modifier = Modifier.height(6.dp))

        Button(
            onClick = onStartNormal,
            enabled = !isRunning,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981))
        ) {
            Text("1. Run Normal Activity (40 Docs)")
        }

        Spacer(modifier = Modifier.height(4.dp))

        Button(
            onClick = onStartModerate,
            enabled = !isRunning,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF59E0B))
        ) {
            Text("2. Run Moderate Suspicious (Renames/Deletes)")
        }

        Spacer(modifier = Modifier.height(4.dp))

        Button(
            onClick = onStartHighIntensity,
            enabled = !isRunning,
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFEF4444))
        ) {
            Text("3. Run High-Intensity Burst (60 Files)")
        }

        Spacer(modifier = Modifier.height(8.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            OutlinedButton(
                onClick = onStop,
                enabled = isRunning,
                modifier = Modifier.weight(1f)
            ) {
                Text("Stop")
            }
            OutlinedButton(
                onClick = onReset,
                enabled = !isRunning && engine.events.isNotEmpty(),
                modifier = Modifier.weight(1f)
            ) {
                Text("Reset")
            }
            Button(
                onClick = onExportCsv,
                enabled = !isRunning && engine.events.isNotEmpty(),
                modifier = Modifier.weight(1f),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF0284C7))
            ) {
                Text("Export")
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        // Event Log Stream
        Text(
            "Live Telemetry Stream (${engine.events.size} events)",
            fontWeight = FontWeight.SemiBold,
            fontSize = 14.sp,
            color = Color(0xFF1E293B)
        )
        Spacer(modifier = Modifier.height(6.dp))

        LazyColumn(
            modifier = Modifier.weight(1f),
            verticalArrangement = Arrangement.spacedBy(6.dp)
        ) {
            items(engine.events.reversed()) { event ->
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = if (event.label == 1) Color(0xFFFEF2F2) else Color.White
                    ),
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(10.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                "${event.operation.uppercase()} | ${event.fileId}",
                                fontWeight = FontWeight.Bold,
                                fontSize = 13.sp
                            )
                            Text(
                                "Size: ${event.fileSize} B | ${event.timestamp}",
                                fontSize = 11.sp,
                                color = Color(0xFF64748B)
                            )
                        }
                        Text(
                            if (event.label == 1) "SUSPICIOUS" else "NORMAL",
                            fontWeight = FontWeight.Bold,
                            fontSize = 11.sp,
                            color = if (event.label == 1) Color(0xFFDC2626) else Color(0xFF16A34A)
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun DiagnosticsScreen(engine: SimulationEngine) {
    val stats = engine.statistics
    val diagnostic = engine.getExplainableDiagnostic()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Diagnostic Card
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(
                containerColor = when (diagnostic.riskLevel) {
                    "HIGH RISK" -> Color(0xFFFEE2E2)
                    "MEDIUM RISK" -> Color(0xFFFEF3C7)
                    else -> Color(0xFFDCFCE7)
                }
            ),
            shape = RoundedCornerShape(12.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    "RISK LEVEL: ${diagnostic.riskLevel}",
                    fontWeight = FontWeight.ExtraBold,
                    fontSize = 16.sp,
                    color = when (diagnostic.riskLevel) {
                        "HIGH RISK" -> Color(0xFFB91C1C)
                        "MEDIUM RISK" -> Color(0xFFB45309)
                        else -> Color(0xFF15803D)
                    }
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    diagnostic.statusSummary,
                    fontWeight = FontWeight.SemiBold,
                    fontSize = 14.sp
                )
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    diagnostic.primaryReason,
                    fontSize = 13.sp,
                    color = Color(0xFF334155)
                )

                if (diagnostic.indicators.isNotEmpty()) {
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "Contributing Behavioral Indicators:",
                        fontWeight = FontWeight.Bold,
                        fontSize = 12.sp
                    )
                    diagnostic.indicators.forEach { indicator ->
                        Text("• $indicator", fontSize = 12.sp, color = Color(0xFF475569))
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            "Aggregated Event Statistics",
            fontWeight = FontWeight.SemiBold,
            fontSize = 15.sp,
            color = Color(0xFF1E293B)
        )

        Spacer(modifier = Modifier.height(8.dp))

        // Stat Grid
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            StatCard(title = "Total Ops", value = "${stats.totalOps}", modifier = Modifier.weight(1f))
            StatCard(title = "Unique Files", value = "${stats.uniqueFiles}", modifier = Modifier.weight(1f))
        }
        Spacer(modifier = Modifier.height(8.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            StatCard(title = "Writes", value = "${stats.writeCount}", modifier = Modifier.weight(1f))
            StatCard(title = "Modifications", value = "${stats.modifyCount}", modifier = Modifier.weight(1f))
        }
        Spacer(modifier = Modifier.height(8.dp))
        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            StatCard(title = "Renames", value = "${stats.renameCount}", modifier = Modifier.weight(1f))
            StatCard(title = "Deletions", value = "${stats.deleteCount}", modifier = Modifier.weight(1f))
        }
    }
}

@Composable
fun StatCard(title: String, value: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = Color.White),
        shape = RoundedCornerShape(8.dp)
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(title, fontSize = 12.sp, color = Color(0xFF64748B))
            Spacer(modifier = Modifier.height(2.dp))
            Text(value, fontSize = 20.sp, fontWeight = FontWeight.Bold, color = Color(0xFF0F172A))
        }
    }
}

@Composable
fun AboutScopeScreen() {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            shape = RoundedCornerShape(12.dp)
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    "Controlled Laboratory Scope",
                    fontWeight = FontWeight.Bold,
                    fontSize = 16.sp,
                    color = Color(0xFF0284C7)
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    "This application is an academic cybersecurity prototype developed for AIORI Hackathon 3 (Problem Statement PS-001) by Team Cipher Aegis.\n\n" +
                    "• Storage Isolation: All file write, modify, rename, and delete operations occur strictly within the application's isolated private sandbox (context.filesDir).\n" +
                    "• User Safety: The app does not inspect, modify, or encrypt any personal photos, documents, or device data.\n" +
                    "• Android Architecture: Modern Android security architecture enforces per-app UID sandboxing. This prototype does not claim device-wide antivirus surveillance, which requires system privileges or dedicated enterprise management APIs.\n" +
                    "• Purpose: To generate safe, reproducible behavioral file-operation telemetry for evaluating rolling-window machine learning early-warning models.",
                    fontSize = 13.sp,
                    color = Color(0xFF334155),
                    lineHeight = 19.sp
                )
            }
        }
    }
}
