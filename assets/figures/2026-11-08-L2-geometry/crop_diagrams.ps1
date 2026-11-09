# Reproduce the two diagram excerpts; the archived original stays unchanged.
# Usage (Windows PowerShell or pwsh on Windows; uses System.Drawing):
#   & ".\crop_diagrams.ps1"
# Rectangles are x, y, width, height in pixels of the 2360x1640 original.
# This copies rectangular excerpts of the handwriting; it does not redraw them.
Add-Type -AssemblyName System.Drawing
$folder = Split-Path -Parent $MyInvocation.MyCommand.Path
$vault  = (Resolve-Path (Join-Path $folder '..\..\..')).Path
$source = Join-Path $vault 'raw\assets\2026-11-08-L2-geometry-I01-conditional-expectation-projection-notes.png'
$expected = 'da948c345719ae3ba4648b79a5e3519bcdc4b5234b11711ce55de98600c73b01'
$actual = (Get-FileHash -Algorithm SHA256 -LiteralPath $source).Hash.ToLower()
if ($actual -ne $expected) { throw "Source hash mismatch: $actual" }
$crops = [ordered]@{
  'I01-excerpt-geometry-in-L2.png'                   = @(14, 628, 362, 274)
  'I01-excerpt-geometry-of-conditional-expectation.png' = @(24, 905, 510, 420)
}
$img = [System.Drawing.Image]::FromFile($source)
try {
  foreach ($name in $crops.Keys) {
    $r = $crops[$name]
    $bmp = [System.Drawing.Bitmap]::new($r[2], $r[3])
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.DrawImage($img, [System.Drawing.Rectangle]::new(0, 0, $r[2], $r[3]),
                 [System.Drawing.Rectangle]::new($r[0], $r[1], $r[2], $r[3]),
                 [System.Drawing.GraphicsUnit]::Pixel)
    $bmp.Save((Join-Path $folder $name), [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
  }
} finally { $img.Dispose() }
