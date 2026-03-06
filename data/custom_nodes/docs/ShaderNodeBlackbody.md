# Blender to Unity: ShaderNodeBlackbody Conversion Guide

## Conversion Type: 2 (Near Conversion)

## Overview
- **Blender Node**: `ShaderNodeBlackbody`
- **Unity ShaderGraph Equivalent**: `Custom Function` Node
- **Category**: Input / Color
- **Compatibility**: 95% (Requires custom implementation)

This document provides a complete guide for recreating the functionality of Blender's `ShaderNodeBlackbody` in Unity using a `Custom Function` node.

## 1. Conceptual Overview
The `ShaderNodeBlackbody` converts a temperature value (in Kelvin) into an approximate RGB color, simulating the light emitted by a heated black body. This is commonly used for physically-based lighting and fire/explosion effects.

Unity's ShaderGraph does not have a built-in node for this calculation. Therefore, we must implement the conversion formula manually using a **`Custom Function`** node and some HLSL code.

## 2. Step-by-Step Recreation in ShaderGraph

### Step 1: Create a Custom Function Node
1.  Right-click on the graph and select **Create Node → Utility → Custom Function**.
2.  Select the new node. In the **Graph Inspector**, click on the cog icon to open its settings.

### Step 2: Configure Inputs and Outputs
1.  **Inputs**: Add one input.
    - **Name**: `Temperature`
    - **Type**: `Vector1`
2.  **Outputs**: Add one output.
    - **Name**: `Color`
    - **Type**: `Vector3`

### Step 3: Add the HLSL Code
1.  In the **Graph Inspector** for the `Custom Function` node, change the **Type** from `File` to `String`.
2.  A text box will appear. Paste the following HLSL code into it. This code contains an industry-standard approximation for converting temperature to RGB.

```hlsl
// Based on algorithm by Tanner Helland
// http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
float3 temperature_rgb = float3(0.0, 0.0, 0.0);
float temp = Temperature / 100.0;

// Red
if (temp <= 66.0) {
    temperature_rgb.r = 255.0;
} else {
    temperature_rgb.r = temp - 60.0;
    temperature_rgb.r = 329.698727446 * pow(temperature_rgb.r, -0.1332047592);
}

// Green
if (temp <= 66.0) {
    temperature_rgb.g = temp;
    temperature_rgb.g = 99.4708025861 * log(temperature_rgb.g) - 161.1195681661;
} else {
    temperature_rgb.g = temp - 60.0;
    temperature_rgb.g = 288.1221695283 * pow(temperature_rgb.g, -0.0755148492);
}

// Blue
if (temp >= 66.0) {
    temperature_rgb.b = 255.0;
} else {
    if (temp <= 19.0) {
        temperature_rgb.b = 0.0;
    } else {
        temperature_rgb.b = temp - 10.0;
        temperature_rgb.b = 138.5177312231 * log(temperature_rgb.b) - 305.0447927307;
    }
}

// Clamp and normalize
temperature_rgb = clamp(temperature_rgb, 0.0, 255.0) / 255.0;
Color = temperature_rgb;
```

3.  Give the function a unique **Name** in the Graph Inspector, like `BlackbodyConversion`.

## 3. Visual Graph Layout
Connect a `Float` property to the `Custom Function` node to control the temperature from the Material Inspector.

```
[Float Property ("Temperature")] --(Out)--> [Custom Function Node].[Temperature]
                                            [Custom Function Node].[Color] --(Out)--> [PBR Master Node].[Emission]
```

## 4. Pseudocode for Conversion Logic
The converter's job is to create and configure the `Custom Function` node automatically.

```python
def convert_blackbody_node(blender_node):
  # 1. Get the input temperature value or connected node.
  temperature_input = get_input_link_or_value(blender_node.inputs["Temperature"])

  # 2. Define the HLSL code for the blackbody conversion.
  hlsl_code = "..." # (The full code from Step 3 above)

  # 3. Create a Custom Function node in ShaderGraph.
  custom_func_node = create_shadergraph_node("Custom Function")
  
  # 4. Configure it.
  custom_func_node.set_function_name("BlackbodyConversion")
  custom_func_node.set_code(hlsl_code)
  custom_func_node.add_input("Temperature", "Vector1")
  custom_func_node.add_output("Color", "Vector3")

  # 5. Connect the temperature input to the new node.
  connect_node(temperature_input, custom_func_node, "output", "Temperature")

  # 6. Return the new custom function node for further connections.
  return custom_func_node
```

## 5. Limitations and Notes
- **Approximation**: The conversion from Kelvin to RGB is an approximation. The provided HLSL code is a widely used standard, but it may have very minor visual differences from Blender's internal implementation at extreme temperature ranges.
- **Flexibility**: Once created, this `Custom Function` node can be saved as a Sub-graph asset (`Create → Shader → Sub-graph`) to be easily reused in other materials without repeating the setup.
- **HDRP**: For High Definition Render Pipeline (HDRP), lighting workflows often deal with temperature directly in the Light components, but if you need this effect in a material, the `Custom Function` method is still the correct approach.
