using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR;
using UnityEngine.XR.Interaction.Toolkit;


[RequireComponent(typeof(CharacterController))]
public class XRMovement : MonoBehaviour
{
    public float speed = 3.0f;
    private XRRig rig;
    private Camera camera;
    private CharacterController characterController;
    private string logSave;


    void Start()
    {
        logSave = "no log";
        rig = GetComponent<XRRig>();
        if (rig == null)
        {
            logSave = "No XRRig found on the object.";
        }
        else
        {
            camera = rig.GetComponentInChildren<Camera>();
            if (camera == null)
            {
                logSave = "No camera found in XRRig or its children.";
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
        // Debug.Log(logSave);
        // Get input from the right thumbstick
        InputDevice rightHandController;
        if (TryGetDeviceWithCharacteristics(InputDeviceCharacteristics.Right | InputDeviceCharacteristics.Controller, out rightHandController))
        {
            Vector2 inputAxis;
            if (rightHandController.TryGetFeatureValue(CommonUsages.primary2DAxis, out inputAxis))
            {
                if (inputAxis != Vector2.zero)
                {
                    // Debug.Log("Right thumbstick input detected: " + inputAxis);  // Log thumbstick input

                    // If we have a valid camera, we can use it to determine the direction
                    if (camera != null)
                    {
                        Vector3 direction = Quaternion.LookRotation(camera.transform.forward, camera.transform.up) * new Vector3(inputAxis.x, 0, inputAxis.y);
                        float inputMagnitude = inputAxis.magnitude;
                        float dynamicSpeed = speed * (1.0f + inputMagnitude);  // Speed will be between speed and 2*speed
                        characterController.Move(dynamicSpeed * Time.deltaTime * direction);
                    }
                }
            }
        }
        else
        {
            // Debug.Log("No right hand controller detected.");  // Log no right hand controller
        }
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
