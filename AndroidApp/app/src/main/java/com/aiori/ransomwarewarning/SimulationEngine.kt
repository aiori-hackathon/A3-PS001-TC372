package com.aiori.ransomwarewarning

import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlinx.coroutines.delay

/**
 * Represents a single file-operation telemetry event generated in the lab.
 * Schema matches the project-wide machine learning dataset format.
 */
data class ActivityEvent(
    val timestamp: String,
    val fileId: String,
    val operation: String,
    val fileSize: Long,
    val scenario: String,
    val label: Int
)

/**
 * Aggregated behavioral statistics across the current simulation run.
 */
data class EventStatistics(
    val totalOps: Int = 0,
    val writeCount: Int = 0,
    val modifyCount: Int = 0,
    val renameCount: Int = 0,
    val deleteCount: Int = 0,
    val uniqueFiles: Int = 0,
    val suspiciousCount: Int = 0,
    val normalCount: Int = 0
)

/**
 * Explainable diagnostic card generated from measured behavioral indicators.
 */
data class ExplainableDiagnostic(
    val riskLevel: String,
    val statusSummary: String,
    val primaryReason: String,
    val indicators: List<String>
)

/**
 * Core controlled laboratory simulation engine.
 * Restricts all file I/O operations strictly to the application's isolated private sandbox.
 */
class SimulationEngine(private val appDirectory: File) {

    val events = mutableListOf<ActivityEvent>()
    private val uniqueFileSet = mutableSetOf<String>()

    var statistics = EventStatistics()
        private set

    fun reset() {
        events.clear()
        uniqueFileSet.clear()
        statistics = EventStatistics()
        
        // Safely purge lab directory
        val labFolder = File(appDirectory, "lab_files")
        if (labFolder.exists()) {
            labFolder.deleteRecursively()
        }
    }

    private fun recordEvent(
        fileId: String,
        operation: String,
        fileSize: Long,
        scenarioName: String,
        suspicious: Boolean
    ): ActivityEvent {
        val timestamp = SimpleDateFormat(
            "yyyy-MM-dd HH:mm:ss.SSS",
            Locale.US
        ).format(Date())

        val event = ActivityEvent(
            timestamp = timestamp,
            fileId = fileId,
            operation = operation.lowercase(Locale.ROOT),
            fileSize = fileSize,
            scenario = scenarioName,
            label = if (suspicious) 1 else 0
        )

        events.add(event)
        uniqueFileSet.add(fileId)

        val writeC = statistics.writeCount + if (operation.equals("write", ignoreCase = true)) 1 else 0
        val modC = statistics.modifyCount + if (operation.equals("modify", ignoreCase = true)) 1 else 0
        val renC = statistics.renameCount + if (operation.equals("rename", ignoreCase = true)) 1 else 0
        val delC = statistics.deleteCount + if (operation.equals("delete", ignoreCase = true)) 1 else 0
        val suspC = statistics.suspiciousCount + if (suspicious) 1 else 0
        val normC = statistics.normalCount + if (!suspicious) 1 else 0

        statistics = EventStatistics(
            totalOps = events.size,
            writeCount = writeC,
            modifyCount = modC,
            renameCount = renC,
            deleteCount = delC,
            uniqueFiles = uniqueFileSet.size,
            suspiciousCount = suspC,
            normalCount = normC
        )

        return event
    }

    suspend fun runNormalSimulation(
        onProgress: (String, ActivityEvent) -> Unit
    ) {
        val folder = File(appDirectory, "lab_files/normal_${System.currentTimeMillis()}")
        folder.mkdirs()
        val scenarioName = "normal_activity"

        for (index in 0 until 40) {
            val file = File(folder, "doc_file_$index.txt")
            file.writeText("Legitimate user document content $index")
            val e1 = recordEvent(file.name, "write", file.length(), scenarioName, false)
            onProgress("Writing document $index/40", e1)
            delay(150)

            file.appendText("\nAdditional ordinary paragraph edit.")
            val e2 = recordEvent(file.name, "modify", file.length(), scenarioName, false)
            onProgress("Editing document $index/40", e2)
            delay(150)
        }
    }

    suspend fun runModerateSimulation(
        onProgress: (String, ActivityEvent) -> Unit
    ) {
        val folder = File(appDirectory, "lab_files/moderate_${System.currentTimeMillis()}")
        folder.mkdirs()
        val scenarioName = "moderate_suspicious"

        for (index in 0 until 40) {
            val file = File(folder, "user_data_$index.txt")
            file.writeText("Controlled lab test data $index")
            val e1 = recordEvent(file.name, "write", file.length(), scenarioName, true)
            onProgress("Write test file $index/40", e1)
            delay(150)

            file.appendText("\nControlled simulated modification.")
            val e2 = recordEvent(file.name, "modify", file.length(), scenarioName, true)
            onProgress("Modify test file $index/40", e2)
            delay(150)

            if (index < 10) {
                val renamed = File(folder, "renamed_data_$index.txt")
                if (file.renameTo(renamed)) {
                    val e3 = recordEvent(renamed.name, "rename", renamed.length(), scenarioName, true)
                    onProgress("Rename burst $index/10", e3)
                    delay(150)

                    if (index < 5 && renamed.delete()) {
                        val e4 = recordEvent(renamed.name, "delete", 0L, scenarioName, true)
                        onProgress("Delete sample $index/5", e4)
                        delay(150)
                    }
                }
            }
        }
    }

    suspend fun runHighIntensitySimulation(
        onProgress: (String, ActivityEvent) -> Unit
    ) {
        val folder = File(appDirectory, "lab_files/high_${System.currentTimeMillis()}")
        folder.mkdirs()
        val scenarioName = "high_intensity_suspicious"

        for (index in 0 until 60) {
            val file = File(folder, "target_file_$index.txt")
            file.writeText("Sensitive simulated document $index")
            val e1 = recordEvent(file.name, "write", file.length(), scenarioName, true)
            onProgress("High velocity write $index/60", e1)
            delay(100)

            repeat(2) { modIdx ->
                file.appendText("\n[ENCRYPTED_SIMULATION_BLOB_$modIdx]")
                val e2 = recordEvent(file.name, "modify", file.length(), scenarioName, true)
                onProgress("High velocity modification $index/60", e2)
                delay(100)
            }

            val lockedFile = File(folder, "target_file_$index.txt.locked")
            if (file.renameTo(lockedFile)) {
                val e3 = recordEvent(lockedFile.name, "rename", lockedFile.length(), scenarioName, true)
                onProgress("Extension append rename $index/60", e3)
                delay(100)

                if (index < 30 && lockedFile.delete()) {
                    val e4 = recordEvent(lockedFile.name, "delete", 0L, scenarioName, true)
                    onProgress("Aggressive wipe delete $index/30", e4)
                    delay(100)
                }
            }
        }
    }

    fun exportToCsvString(): String {
        return buildString {
            appendLine("timestamp,file_id,operation,file_size,scenario_type,label")
            events.forEach { event ->
                appendLine(
                    "${event.timestamp},${event.fileId}," +
                    "${event.operation},${event.fileSize}," +
                    "${event.scenario},${event.label}"
                )
            }
        }
    }

    fun getExplainableDiagnostic(): ExplainableDiagnostic {
        val s = statistics
        val indicators = mutableListOf<String>()

        if (s.renameCount >= 5) {
            indicators.add("Abnormal file renaming burst (${s.renameCount} renames)")
        }
        if (s.modifyCount >= 15 && (s.renameCount > 0 || s.deleteCount > 0 || s.suspiciousCount > 0)) {
            indicators.add("High-frequency in-place modification burst (${s.modifyCount} modifies)")
        }
        if (s.deleteCount >= 5) {
            indicators.add("Unusual batch deletion pattern (${s.deleteCount} deletes)")
        }
        if (s.uniqueFiles >= 15 && (s.renameCount > 0 || s.deleteCount > 0)) {
            indicators.add("Wide filesystem spread across ${s.uniqueFiles} unique files")
        }

        return when {
            s.totalOps == 0 -> ExplainableDiagnostic(
                riskLevel = "NORMAL",
                statusSummary = "System Idle",
                primaryReason = "No file operations recorded yet.",
                indicators = emptyList()
            )
            s.suspiciousCount == 0 -> ExplainableDiagnostic(
                riskLevel = "NORMAL",
                statusSummary = "Benign Legitimate Activity",
                primaryReason = "File operation patterns conform to ordinary document editing and backup rates.",
                indicators = listOf("Low operation velocity", "No suspicious renaming or mass deletion observed")
            )
            s.renameCount >= 10 || s.deleteCount >= 10 -> ExplainableDiagnostic(
                riskLevel = "HIGH RISK",
                statusSummary = "Ransomware-Like Activity Burst Detected",
                primaryReason = "Detected concurrent high-frequency modification, file extension renaming, and deletion.",
                indicators = indicators
            )
            else -> ExplainableDiagnostic(
                riskLevel = "MEDIUM RISK",
                statusSummary = "Moderate Behavioral Anomaly",
                primaryReason = "Unusual increase in operational frequency and modification/rename behavior.",
                indicators = indicators
            )
        }
    }
}
