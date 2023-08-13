using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(CharacterController))]
public class ControllerMovement : MonoBehaviour
{
    public float speed = 3.0f;
    public float rotationSpeed = 3.0f;
    private CharacterController characterController;
    private string logSave;

    void Start()
    {
        logSave = "ControllerMovement script is active.";  // Log that script is active
        characterController = GetComponent<CharacterController>();
    }

    void Update()
    {
        // Handle Controller Inputs
        HandleControllerInputs();
    }

    void HandleControllerInputs()
    {
        // Debug.Log(logSave);

        // Vertical Movement - Left stick
        Vector2 inputAxisLeft = new Vector2(Input.GetAxis("Horizontal"), Input.GetAxis("Vertical"));

        if (inputAxisLeft.y != 0)
        {
            // Debug.Log("Left thumbstick input detected: " + inputAxisLeft);  // Log thumbstick input

            // Move the characterController vertically
            Vector3 verticalMovement = new Vector3(0, 0, inputAxisLeft.y);
            characterController.SimpleMove(speed * transform.TransformDirection(verticalMovement));
        }

        // Horizontal Movement - Right Stick
        Vector2 inputAxisRight = new Vector2(Input.GetAxis("RightStickHorizontal"), Input.GetAxis("RightStickVertical"));
        if (inputAxisRight.x != 0)
        {
            // Rotate the camera based on right stick horizontal movement
            transform.Rotate(new Vector3(0, inputAxisRight.x, 0) * rotationSpeed);
        }

        // Time Scale Change - Left Stick Horizontal
        if (inputAxisLeft.x != 0)
        {
            // Adjust time scale based on left stick horizontal movement
            float timeScaleChangeSpeed = 0.1f;  // Change this value to control how quickly time scale changes
            Time.timeScale += inputAxisLeft.x * timeScaleChangeSpeed * Time.deltaTime;
            Time.timeScale = Mathf.Clamp(Time.timeScale, 0.1f, 2f);  // Clamp between 0.1 (slow motion) and 2 (double speed)

            // Adjust fixed delta time in accordance with time scale
            Time.fixedDeltaTime = 0.02f * Time.timeScale;
        }
    }
}
