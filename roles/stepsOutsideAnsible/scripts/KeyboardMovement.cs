using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(CharacterController))]
public class KeyboardMovement : MonoBehaviour
{
    public float speed = 3.0f;
    private Camera camera;
    private CharacterController characterController;
    private string logSave;
    public float rotationSpeed = 1.0f; // Speed of camera rotation


    private float pitch = 0.0f; // Vertical rotation
    private float yaw = 0.0f;   // Horizontal rotation

    void Start()
    {
        logSave = "KeyboardMovement script is active.";  // Log that script is active
        camera = Camera.main;
        characterController = GetComponent<CharacterController>();
    }

    void Update()
    {
        // Handle Keyboard and Mouse Inputs
        HandleKeyboardAndMouseInputs();
    }

    void HandleKeyboardAndMouseInputs()
    {
        // Debug.Log(logSave);

        // Handle Vertical Movement (W/S or Up/Down)
        if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow))
        {
            Vector3 forwardMovement = new Vector3(0, 0, 1);
            characterController.Move(speed * Time.deltaTime * camera.transform.TransformDirection(forwardMovement));
        }
        if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow))
        {
            Vector3 backwardMovement = new Vector3(0, 0, -1);
            characterController.Move(speed * Time.deltaTime * camera.transform.TransformDirection(backwardMovement));
        }

        // Handle Horizontal Movement (A/D or Left/Right)
        if (Input.GetKey(KeyCode.A) || Input.GetKey(KeyCode.LeftArrow))
        {
            Vector3 leftMovement = new Vector3(-1, 0, 0);
            characterController.Move(speed * Time.deltaTime * camera.transform.TransformDirection(leftMovement));
        }
        if (Input.GetKey(KeyCode.D) || Input.GetKey(KeyCode.RightArrow))
        {
            Vector3 rightMovement = new Vector3(1, 0, 0);
            characterController.Move(speed * Time.deltaTime * camera.transform.TransformDirection(rightMovement));
        }

        // Handle vertical rising and descending (Space/Ctrl)
        if (Input.GetKey(KeyCode.Space))
        {
            Vector3 riseMovement = new Vector3(0, 1, 0);
            characterController.Move(speed * Time.deltaTime * camera.transform.TransformDirection(riseMovement));
        }
        if (Input.GetKey(KeyCode.LeftControl))
        {
            Vector3 descendMovement = new Vector3(0, -1, 0);
            characterController.Move(speed * Time.deltaTime * camera.transform.TransformDirection(descendMovement));
        }


        // Change time scale based on Mouse Scroll Wheel
        float timeScaleChangeSpeed = 0.1f;
        Time.timeScale += Input.mouseScrollDelta.y * timeScaleChangeSpeed;
        Time.timeScale = Mathf.Clamp(Time.timeScale, 0.1f, 2f);  // Clamp between 0.1 (slow motion) and 2 (double speed)

        // Adjust fixed delta time in accordance with time scale
        Time.fixedDeltaTime = 0.02f * Time.timeScale;

        // Rotate the Camera based on Mouse Movement
        if (Input.GetMouseButton(1)) // Right mouse button
        {
            float mouseX = Input.GetAxis("Mouse X");
            float mouseY = Input.GetAxis("Mouse Y");

            yaw += mouseX * rotationSpeed;
            pitch += mouseY * rotationSpeed;

            // Ensure the vertical rotation stays between -90 and 90 degrees
            pitch = Mathf.Clamp(pitch, -90f, 90f);

            // Apply the rotation to the camera
            camera.transform.localRotation = Quaternion.Euler(pitch, yaw, 0);
        }

    }
}
