# 🎯 API Positioning Guide - Control Name & Address Placement

This guide shows you how to control the exact position of the name and address on your PDF pages via the API, just like you can in the web interface.

## 📐 Understanding the Coordinate System

### Page Dimensions
- **Format:** A4 (210mm × 297mm)
- **Origin:** Bottom-left corner is (0, 0)
- **Units:** All measurements are in **millimeters (mm)**

### Position Object Structure
```json
{
  "left": 20,      // Distance from left edge (0-210mm)
  "bottom": 250,   // Distance from bottom edge (0-297mm)
  "width": 80,     // Width of the text area
  "height": 30     // Height of the text area
}
```

## 🎨 Default Positions

These are the same positions used by the web interface by default:

**Name Zone (Green):**
```json
{
  "left": 20,
  "bottom": 250,
  "width": 80,
  "height": 30
}
```
- Position: Top-left area
- Good for: Name/header text

**Address Zone (Blue):**
```json
{
  "left": 95,
  "bottom": 20,
  "width": 100,
  "height": 40
}
```
- Position: Bottom-right area
- Good for: Envelope window alignment

## 📝 API Usage

### Basic Example with Custom Positions

```bash
curl -X POST https://csv-to-pdf-9i9b.onrender.com/api/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "John Doe",
        "address": "123 Main Street\nNew York, NY 10001\nUSA"
      }
    ],
    "namePosition": {
      "left": 20,
      "bottom": 250,
      "width": 80,
      "height": 30
    },
    "addressPosition": {
      "left": 95,
      "bottom": 20,
      "width": 100,
      "height": 40
    },
    "singleFile": true
  }' \
  -o output.pdf
```

## 🎯 Common Layout Patterns

### 1. Standard Envelope Window Layout
Perfect for standard envelope windows (bottom-right):

```json
{
  "namePosition": {
    "left": 20,
    "bottom": 250,
    "width": 80,
    "height": 30
  },
  "addressPosition": {
    "left": 95,
    "bottom": 20,
    "width": 100,
    "height": 40
  }
}
```

### 2. Top-Left Name, Bottom-Left Address
Good for custom layouts:

```json
{
  "namePosition": {
    "left": 20,
    "bottom": 270,
    "width": 100,
    "height": 20
  },
  "addressPosition": {
    "left": 20,
    "bottom": 20,
    "width": 120,
    "height": 50
  }
}
```

### 3. Centered Layout
Both zones centered:

```json
{
  "namePosition": {
    "left": 80,
    "bottom": 250,
    "width": 50,
    "height": 30
  },
  "addressPosition": {
    "left": 55,
    "bottom": 100,
    "width": 100,
    "height": 60
  }
}
```

### 4. Full-Width Address
Address spans most of the page width:

```json
{
  "namePosition": {
    "left": 20,
    "bottom": 250,
    "width": 80,
    "height": 30
  },
  "addressPosition": {
    "left": 20,
    "bottom": 20,
    "width": 170,
    "height": 60
  }
}
```

## 🔧 Finding the Perfect Position

### Method 1: Use the Web Interface
1. Go to `https://csv-to-pdf-9i9b.onrender.com/`
2. Upload a test CSV and PDF
3. Drag and resize the zones to your desired positions
4. Check the coordinate panel on the right
5. Copy the exact values into your API call

### Method 2: Calculate from Requirements

**Example:** You want the address 30mm from left, 25mm from bottom, 90mm wide, 45mm tall:

```json
{
  "addressPosition": {
    "left": 30,      // 30mm from left
    "bottom": 25,    // 25mm from bottom
    "width": 90,     // 90mm wide
    "height": 45     // 45mm tall
  }
}
```

### Method 3: Trial and Error
Start with default positions and adjust incrementally:

```bash
# Test with default
curl ... -d '{"data": [...], "namePosition": {"left": 20, "bottom": 250, "width": 80, "height": 30}}'

# Adjust left by 10mm
curl ... -d '{"data": [...], "namePosition": {"left": 30, "bottom": 250, "width": 80, "height": 30}}'

# Adjust bottom by 20mm
curl ... -d '{"data": [...], "namePosition": {"left": 30, "bottom": 230, "width": 80, "height": 30}}'
```

## ⚠️ Important Constraints

### Boundaries
- **left**: Must be between 0 and (210 - width)
- **bottom**: Must be between 0 and (297 - height)
- **width**: Must be > 0 and ≤ (210 - left)
- **height**: Must be > 0 and ≤ (297 - bottom)

### Example Validations
```json
// ✅ Valid
{
  "left": 20,
  "bottom": 250,
  "width": 80,
  "height": 30
}
// left + width = 100 < 210 ✓
// bottom + height = 280 < 297 ✓

// ❌ Invalid (would overflow)
{
  "left": 150,
  "bottom": 250,
  "width": 80,  // 150 + 80 = 230 > 210 ✗
  "height": 30
}
```

## 🎨 Visual Reference

```
A4 Page (210mm × 297mm)
┌─────────────────────────────────────┐
│                                     │ ← Top (297mm)
│                                     │
│  [Name Zone]                        │
│  (default: left=20, bottom=250)     │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
│                                     │
│              [Address Zone]         │
│              (default: left=95,     │
│               bottom=20)            │
└─────────────────────────────────────┘
← Left (0mm)                    Right (210mm) →
```

## 📊 Position Examples by Use Case

### Envelope Window (Standard)
```json
{
  "addressPosition": {
    "left": 95,
    "bottom": 20,
    "width": 100,
    "height": 40
  }
}
```

### Business Card Style
```json
{
  "namePosition": {
    "left": 20,
    "bottom": 200,
    "width": 170,
    "height": 30
  },
  "addressPosition": {
    "left": 20,
    "bottom": 150,
    "width": 170,
    "height": 60
  }
}
```

### Letterhead Style
```json
{
  "namePosition": {
    "left": 20,
    "bottom": 270,
    "width": 100,
    "height": 20
  },
  "addressPosition": {
    "left": 20,
    "bottom": 20,
    "width": 100,
    "height": 50
  }
}
```

## 🔄 Omitting Positions

If you don't specify `namePosition` or `addressPosition`, the API uses the default values (same as web interface).

```json
{
  "data": [{"name": "Test", "address": "123 Main St"}],
  "singleFile": true
  // Uses default positions automatically
}
```

## 📚 Complete Example

```bash
curl -X POST https://csv-to-pdf-9i9b.onrender.com/api/generate \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "name": "John Doe",
        "address": "123 Main Street\nNew York, NY 10001\nUSA"
      },
      {
        "name": "Jane Smith",
        "address": "456 Oak Avenue\nLos Angeles, CA 90001\nUSA"
      }
    ],
    "namePosition": {
      "left": 20,
      "bottom": 250,
      "width": 80,
      "height": 30
    },
    "addressPosition": {
      "left": 95,
      "bottom": 20,
      "width": 100,
      "height": 40
    },
    "singleFile": false
  }' \
  -o output.zip
```

## 🆘 Troubleshooting

### Text is cut off
- Increase `width` or `height`
- Check that `left + width ≤ 210`
- Check that `bottom + height ≤ 297`

### Text is in wrong position
- Remember: `bottom` is distance from **bottom edge**, not top
- Higher `bottom` value = higher on page
- `left` is distance from **left edge**

### Position not working
- Verify JSON syntax is correct
- Check that all four values (left, bottom, width, height) are provided
- Ensure values are numbers, not strings

---

**Need help?** Use the web interface at `https://csv-to-pdf-9i9b.onrender.com/` to visually position elements, then copy the coordinates to your API calls!

