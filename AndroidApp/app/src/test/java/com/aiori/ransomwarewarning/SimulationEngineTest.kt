package com.aiori.ransomwarewarning

import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import java.io.File
import java.nio.file.Files

class SimulationEngineTest {

    private lateinit var tempDir: File
    private lateinit var engine: SimulationEngine

    @Before
    fun setUp() {
        tempDir = Files.createTempDirectory("android_sim_test").toFile()
        engine = SimulationEngine(tempDir)
    }

    @Test
    fun testInitialState() {
        assertEquals(0, engine.events.size)
        assertEquals(0, engine.statistics.totalOps)
        assertEquals("NORMAL", engine.getExplainableDiagnostic().riskLevel)
    }

    @Test
    fun testNormalSimulationGeneratesValidEvents() = runBlocking {
        engine.runNormalSimulation { _, _ -> }

        // Normal simulation generates 40 files, with 1 write + 1 modify each = 80 events
        assertEquals(80, engine.events.size)
        assertEquals(80, engine.statistics.totalOps)
        assertEquals(40, engine.statistics.writeCount)
        assertEquals(40, engine.statistics.modifyCount)
        assertEquals(0, engine.statistics.renameCount)
        assertEquals(0, engine.statistics.deleteCount)
        assertEquals(0, engine.statistics.suspiciousCount)
        assertEquals(80, engine.statistics.normalCount)

        // Diagnostic must be NORMAL
        val diagnostic = engine.getExplainableDiagnostic()
        assertEquals("NORMAL", diagnostic.riskLevel)
        assertTrue(diagnostic.statusSummary.contains("Benign"))
    }

    @Test
    fun testModerateSimulationGeneratesSuspiciousEvents() = runBlocking {
        engine.runModerateSimulation { _, _ -> }

        // 40 writes + 40 modifies + 10 renames + 5 deletes = 95 events
        assertEquals(95, engine.events.size)
        assertEquals(40, engine.statistics.writeCount)
        assertEquals(40, engine.statistics.modifyCount)
        assertEquals(10, engine.statistics.renameCount)
        assertEquals(5, engine.statistics.deleteCount)
        assertEquals(95, engine.statistics.suspiciousCount)

        val diagnostic = engine.getExplainableDiagnostic()
        // Rename >= 10 triggers HIGH RISK diagnostic
        assertEquals("HIGH RISK", diagnostic.riskLevel)
        assertTrue(diagnostic.indicators.any { it.contains("renaming") })
    }

    @Test
    fun testCsvExportSchemaMatchesModelRequirements() = runBlocking {
        engine.runNormalSimulation { _, _ -> }
        val csv = engine.exportToCsvString()

        val lines = csv.trim().lines()
        assertTrue(lines.isNotEmpty())
        assertEquals("timestamp,file_id,operation,file_size,scenario_type,label", lines[0])

        val firstDataRow = lines[1].split(",")
        assertEquals(6, firstDataRow.size)
        // Verify label is integer 0 or 1
        val labelVal = firstDataRow[5].toInt()
        assertEquals(0, labelVal)
    }

    @Test
    fun testResetClearsEventsAndStorage() = runBlocking {
        engine.runNormalSimulation { _, _ -> }
        assertTrue(engine.events.isNotEmpty())

        engine.reset()
        assertEquals(0, engine.events.size)
        assertEquals(0, engine.statistics.totalOps)
        assertFalse(File(tempDir, "lab_files").exists())
    }
}
