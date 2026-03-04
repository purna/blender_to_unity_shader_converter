# Pre-Export Analysis Panel - Visual Guide

## NEW FEATURE: Material Properties Panel Shows Issues Before Export

When you select a material with shader nodes, a new panel appears showing all conversion issues.

---

## Where to Find the Panel

```
Blender Interface
└─ Properties Panel (Right side)
   └─ Material Properties Tab
      └─ "Shader Conversion Analysis" Panel ← NEW!
```

### Visual Layout

```
┌─────────────────────────────────────────────────────────┐
│  Material Properties                                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🛈 Shader Conversion Analysis                          │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  Conversion Success Rate:                      ✓ 75%   │
│  Total Nodes: 8                                         │
│                                                         │
│  Node Breakdown:              🔗                        │
│    ✓ Direct: 5               ⊕ Decompose: 2           │
│    ≈ Approximated: 1         ✗ Incompatible: 0        │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  ⚠ Warnings (2)                                    ⓘ    │
│    • Type mismatch: VALUE → VECTOR                     │
│    • Unsupported node: Ambient Occlusion              │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  💡 Recommendations                                  ⓘ   │
│    • Remove incompatible nodes                        │
│    • Consider simplifying shader for better compat.   │
│                                                         │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│          ┌────────────────────────────────────┐        │
│          │ 📤 Export to Unity                 │        │
│          └────────────────────────────────────┘        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## What Information It Shows

### 1️⃣ Conversion Success Rate
```
Conversion Success Rate: ✓ 75%
```
Overall percentage of nodes that can be successfully converted.

### 2️⃣ Node Statistics
```
Total Nodes: 8

Node Breakdown:
  ✓ Direct: 5           (1:1 mapping, perfect)
  ⊕ Decompose: 2       (split into multiple nodes)
  ≈ Approximated: 1    (mathematical approximation)
  ✗ Incompatible: 0    (cannot convert)
```

### 3️⃣ Incompatible Nodes (if any)
```
⚠ Incompatible Nodes
  • AmbientOcclusion (ShaderNodeAmbientOcclusion)
  • LightPath (ShaderNodeLightPath)
```

### 4️⃣ Warnings
```
⚠ Warnings (3)
  • Type mismatch: VALUE → VECTOR
  • Unsupported node: Ambient Occlusion
  • Complex blend mode detected: OVERLAY
  ... and 0 more warnings
```

### 5️⃣ Recommendations
```
💡 Recommendations
  • Remove or replace incompatible nodes
  • Check socket type connections
  • Consider simplifying shader for better compatibility
```

### 6️⃣ Quick Export Button
```
┌────────────────────────────────────┐
│ 📤 Export to Unity                 │
└────────────────────────────────────┘
```
Direct export from the panel without going to File > Export menu.

---

## Step-by-Step: Using the Analysis Panel

### Step 1: Create/Select Material

1. Create a material with shader nodes
2. Make sure "Use Nodes" is enabled
3. Add your shader nodes (Principled BSDF, textures, etc.)

### Step 2: Select the Object

Click on an object that has this material applied.

### Step 3: Open Material Properties

In the **Properties Panel** on the right:
```
Click the Material Properties icon (sphere icon)
```

### Step 4: Scroll to "Shader Conversion Analysis"

The panel will appear automatically if:
- ✓ You have a material selected
- ✓ Material uses shader nodes
- ✓ You're in the Material Properties tab

### Step 5: Review the Analysis

```
╔════════════════════════════════════════════════╗
║   Read Success Rate                            ║
║   Check Node Breakdown                         ║
║   Review any Incompatible Nodes                ║
║   Address Warnings if any                      ║
║   Follow Recommendations                       ║
╚════════════════════════════════════════════════╝
```

### Step 6: Make Adjustments (Optional)

If there are issues:
- Remove incompatible nodes
- Fix type mismatches by adding converter nodes
- Simplify complex shaders

### Step 7: Export

Click **"Export to Unity"** button in the panel, or:
- **File → Export → "Blender Shader to Unity (.fbx + .shadergraph)"**

---

## Example: What You Might See

### Example 1: Good Shader (High Success)

```
┌─────────────────────────────────────────────────────────┐
│  Shader Conversion Analysis                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Conversion Success Rate:                      ✓ 90%   │
│  Total Nodes: 5                                         │
│                                                         │
│  Node Breakdown:                                        │
│    ✓ Direct: 4               ⊕ Decompose: 1           │
│    ≈ Approximated: 0         ✗ Incompatible: 0        │
│                                                         │
│  (No incompatible nodes)                                │
│  (No warnings)                                          │
│  (No recommendations)                                   │
│                                                         │
│          ┌────────────────────────────────────┐        │
│          │ 📤 Export to Unity                 │        │
│          └────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

✅ **Safe to export!**

### Example 2: Okay Shader (Medium Success)

```
┌─────────────────────────────────────────────────────────┐
│  Shader Conversion Analysis                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Conversion Success Rate:                      ✓ 70%   │
│  Total Nodes: 10                                        │
│                                                         │
│  Node Breakdown:                                        │
│    ✓ Direct: 6               ⊕ Decompose: 2           │
│    ≈ Approximated: 1         ✗ Incompatible: 1        │
│                                                         │
│  ⚠ Incompatible Nodes                                  │
│    • AmbientOcclusion (ShaderNodeAmbientOcclusion)    │
│                                                         │
│  ⚠ Warnings (2)                                         │
│    • Type mismatch: VALUE → VECTOR                     │
│    • Unsupported feature: Hair Info                    │
│                                                         │
│  💡 Recommendations                                     │
│    • Remove incompatible nodes                         │
│    • Check socket type connections                     │
│                                                         │
│          ┌────────────────────────────────────┐        │
│          │ 📤 Export to Unity                 │        │
│          └────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

⚠️ **Can export, but review warnings first**

### Example 3: Complex Shader (Low Success)

```
┌─────────────────────────────────────────────────────────┐
│  Shader Conversion Analysis                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Conversion Success Rate:                      ✓ 45%   │
│  Total Nodes: 20                                        │
│                                                         │
│  Node Breakdown:                                        │
│    ✓ Direct: 7               ⊕ Decompose: 2           │
│    ≈ Approximated: 4         ✗ Incompatible: 7        │
│                                                         │
│  ⚠ Incompatible Nodes                                  │
│    • Ambient Occlusion (ShaderNodeAmbientOcclusion)   │
│    • Light Path (ShaderNodeLightPath)                 │
│    • Volumetric Scatter (ShaderNodeVolumeScatter)     │
│    • Hair Info (ShaderNodeHairInfo)                   │
│    • Point Density (ShaderNodeTexPointDensity)        │
│    • Cryptomatte (ShaderNodeCryptomatte)              │
│    • Light Falloff (ShaderNodeLightFalloff)           │
│                                                         │
│  ⚠ Warnings (9)                                         │
│    • Unsupported: Ambient Occlusion                    │
│    • Unsupported: Light Path                          │
│    • Type mismatch: SHADER → VALUE                     │
│    • Complex blend mode detected: OVERLAY              │
│    • ... and 5 more warnings                           │
│                                                         │
│  💡 Recommendations                                     │
│    • Remove or replace incompatible nodes              │
│    • Check socket type connections                     │
│    • Consider simplifying shader for better compat.   │
│                                                         │
│          ┌────────────────────────────────────┐        │
│          │ 📤 Export to Unity                 │        │
│          └────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

❌ **Recommend fixing issues before export**

---

## How Analysis Works (Technical)

### Behind the Scenes

```python
# When you select a material, the panel:

1. Parses the shader graph (parser.py)
   └─ Extracts all nodes and connections

2. Loads node database (utils.load_node_mappings)
   └─ Reads node_mappings.json

3. Analyzes each node
   └─ Looks up strategy from JSON
   └─ Categorizes: direct/decompose/approximate/incompatible

4. Checks connections
   └─ Validates socket types
   └─ Finds mismatches

5. Calculates success rate
   └─ (convertible_nodes / total_nodes) * 100

6. Displays all information in panel
   └─ Updates in real-time as you edit shader
```

---

## Real-Time Updates

The panel updates **automatically** as you edit:

```
You edit shader
    ↓
Panel detects change
    ↓
Re-analyzes shader
    ↓
Updates statistics
    ↓
Shows new issues/recommendations
```

No manual refresh needed - it all updates live!

---

## Benefits of Pre-Export Analysis

✅ **See issues before exporting** - Don't waste time on failed conversions  
✅ **Get recommendations** - Know what to fix  
✅ **Real-time feedback** - Edit and see changes instantly  
✅ **Success rate** - Know how compatible your shader is  
✅ **Quick export** - Button right in the panel  
✅ **Detailed warnings** - Know exactly what's wrong  

---

## What Gets Analyzed

The panel analyzes:

| Item | What's Checked |
|------|----------------|
| **Nodes** | Type, conversion strategy, compatibility |
| **Connections** | Socket type compatibility |
| **Parameters** | Value ranges, texture references |
| **Overall** | Success rate, warnings, recommendations |

---

## Tips for Best Results

1. **Use Principled BSDF** - Best compatibility
2. **Avoid volumetric effects** - Not supported in real-time
3. **Keep it simple** - Fewer nodes = better conversion
4. **Use standard textures** - Image textures have 95% compatibility
5. **Check socket types** - Fix mismatches shown in panel
6. **Review warnings** - Address them before export

---

## Summary

The **Shader Conversion Analysis Panel** gives you:

✅ Pre-export preview of all issues  
✅ Success rate percentage  
✅ Node-by-node breakdown  
✅ Incompatible node list  
✅ Type mismatch warnings  
✅ Actionable recommendations  
✅ Real-time updates as you edit  
✅ Quick export button  

**Use it to make informed decisions before exporting!**
