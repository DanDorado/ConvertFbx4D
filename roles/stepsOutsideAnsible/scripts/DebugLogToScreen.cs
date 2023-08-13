using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class DebugLogToScreen : MonoBehaviour
{
    public TMP_Text debugText;

    private string log = "";

    void Start()
    {
        debugText.text = "Debug Text Initialized"; // hardcoded string
    }

    void OnEnable()
    {
        Application.logMessageReceived += HandleLog;
    }

    void OnDisable()
    {
        Application.logMessageReceived -= HandleLog;
    }

    void HandleLog(string logString, string stackTrace, LogType type)
    {
        log = logString;
        debugText.text = log;
    }
}
