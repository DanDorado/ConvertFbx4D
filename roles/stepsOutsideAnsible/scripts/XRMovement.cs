using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using Unity.XR.CoreUtils;


[RequireComponent(typeof(CharacterController))]
public class XRMovement : MonoBehaviour
{
    public float speed = 3.0f;
    private XROrigin rig;
    private Camera camera;
    private CharacterController characterController;
    private string logSave;

    void Start()
    {

        logSave = "no log";
        rig = GetComponent<XROrigin>();
        if (rig == null)
        {
            logSave = "No XROrigin found on the object.";
        }
        else
        {
            camera = rig.GetComponentInChildren<Camera>();
            if (camera == null)
            {
                logSave = "No camera found in XROrigin or its children.";
            }
            else
            {
                logSave = "XRMovement script is active.";  // Log that script is active
            }
        }
        characterController = GetComponent<CharacterController>();
    }

    void Update()
    {

        // Handle XR Controller Inputs
        HandleXRInputs();

    }

    void HandleXRInputs()
    {
        // Debug.Log(logSave);
        // Get input from the right thumbstick


       // Get input from the left thumbstick
        InputDevice leftHandController;
        if (TryGetDeviceWithCharacteristics(InputDeviceCharacteristics.Left | InputDeviceCharacteristics.Controller, out leftHandController))
        {
            Vector2 inputAxisLeft;
            if (leftHandController.TryGetFeatureValue(CommonUsages.primary2DAxis, out inputAxisLeft))
            {

                if (inputAxisLeft.y != 0)
                {
                    // Debug.Log("Left thumbstick input detected: " + inputAxisLeft);  // Log thumbstick input

                    // Move the characterController vertically
                    Vector3 verticalMovement = new Vector3(0, inputAxisLeft.y, 0);
                    characterController.Move(speed * Time.deltaTime * transform.InverseTransformDirection(verticalMovement));
                }

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
        else
        {
            // Debug.Log("No left hand controller detected.");  // Log no left hand controller
        }


        InputDevice rightHandController;
        if (TryGetDeviceWithCharacteristics(InputDeviceCharacteristics.Right | InputDeviceCharacteristics.Controller, out rightHandController))
        {
            Vector2 inputAxisRight;
            if (rightHandController.TryGetFeatureValue(CommonUsages.primary2DAxis, out inputAxisRight))
            {
                if (inputAxisRight != Vector2.zero)
                {
                    // Debug.Log("Right thumbstick input detected: " + inputAxisRight);  // Log thumbstick input

                    // If we have a valid camera, we can use it to determine the direction
                    if (camera != null)
                    {
                        Vector3 direction = Quaternion.Euler(0, camera.transform.eulerAngles.y, 0) * new Vector3(inputAxisRight.x, 0, inputAxisRight.y);
                        characterController.Move(speed * Time.deltaTime * direction);
                    }
                }
            }
        }
        else
        {
            // Debug.Log("No right hand controller detected.");  // Log no right hand controller
        }

        // Debug.Log("Left Controller: " + leftHandController.name + " Right Controller: " + rightHandController.name);

    }

    bool TryGetDeviceWithCharacteristics(InputDeviceCharacteristics inputDeviceCharacteristics, out InputDevice device)
    {
        List<InputDevice> devices = new List<InputDevice>();
        InputDevices.GetDevicesWithCharacteristics(inputDeviceCharacteristics, devices);
        if (devices.Count > 0)
        {
            device = devices[0];
            return true;
        }
        else
        {
            device = new InputDevice();
            return false;
        }
    }
}
