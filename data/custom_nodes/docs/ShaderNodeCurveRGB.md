# ShaderNodeCurveRGB

## Overview
Blender's RGB Curves node allows per-channel curve adjustments (like Photoshop Curves). Each R, G, B channel can have its input-output relationship modified independently.

## Unity Equivalent
- **Best Option**: Curve properties (one per channel) + channel separation
- **Alternative**: Custom Function with HLSL curve evaluation

## Conversion Process

### Approach 1: Per-Channel Curve Properties (Recommended)
This approach creates separate Curve properties for each channel.

**Step 1: Separate Color Channels**
- Use [Separate Color] node to split RGB into R, G, B channels

**Step 2: Create Curve Properties**
- Create 3 Curve properties: `RedCurve`, `GreenCurve`, `BlueCurve`
- Each curve maps input [0-1] to output [0-1]

**Step 3: Apply Curves**
- Connect R → RedCurve → R output
- Connect G → GreenCurve → G output  
- Connect B → BlueCurve → B output

**Step 4: Recombine**
- Use [Combine Color] node to merge R, G, B back together

### Approach 2: Custom Function (Advanced)
For exact Blender curve behavior, implement HLSL curve evaluation.

**Step 1: Extract Control Points**
- Parse Blender curve control points
- Store as float2 array in shader

**Step 2: Implement Evaluation Function**
```hlsl
float EvaluateCurve(float input, float2 points[4]) {
    // Linear interpolation between control points
    // Or cubic spline evaluation for smooth curves
}
```

**Step 3: Apply to Each Channel**
- Call function for R, G, B separately

## Compatibility: 50%

## Implementation Details

### Unity Node Setup (Approach 1):
```
[Color Input]
      ↓
[Separate Color] → R, G, B
      ↓
[Curve Property: Red]   [Curve Property: Green]   [Curve Property: Blue]
      ↓                    ↓                         ↓
      └────────────────┬────┴─────────────────────┘
                      ↓
              [Combine Color]
                      ↓
               [Color Output]
```

### Build Instructions:
1. Create "Separate Color" node
2. Create 3 Curve properties (RedCurve, GreenCurve, BlueCurve)
3. Create 3 "Branch" nodes or use Multiply with curve outputs
4. Create "Combine Color" node
5. Wire: Color → Separate → Curves → Combine → Output

## Limitations
- Complex spline curves require Custom Function
- Linear approximation for simple curves
- Control point count limited in Unity Curve property
