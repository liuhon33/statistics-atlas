# Original diagram by Codex. Run with PowerShell on Windows; uses System.Drawing.
Add-Type -AssemblyName System.Drawing
$b=[System.Drawing.Bitmap]::new(1500,720)
$g=[System.Drawing.Graphics]::FromImage($b)
$g.SmoothingMode='AntiAlias'
$g.Clear([System.Drawing.Color]::FromArgb(248,250,253))
function Txt($s,$x,$y,$size=22,$color='#253650') {
    $f=[System.Drawing.Font]::new('Segoe UI',$size)
    $br=[System.Drawing.SolidBrush]::new([System.Drawing.ColorTranslator]::FromHtml($color))
    $sf=[System.Drawing.StringFormat]::new(); $sf.Alignment='Center'
    $g.DrawString($s,$f,$br,[single]$x,[single]$y,$sf)
    $f.Dispose(); $br.Dispose(); $sf.Dispose()
}
function Box($s,$x,$y,$w,$color) {
    $p=[System.Drawing.Pen]::new([System.Drawing.ColorTranslator]::FromHtml($color),3)
    $g.FillRectangle([System.Drawing.Brushes]::White,($x-$w/2),$y,$w,75)
    $g.DrawRectangle($p,($x-$w/2),$y,$w,75)
    Txt $s $x ($y+18) 21 $color
    $p.Dispose()
}
function Arr($x1,$y1,$x2,$y2) {
    $p=[System.Drawing.Pen]::new([System.Drawing.Color]::SlateGray,3)
    $cap=[System.Drawing.Drawing2D.AdjustableArrowCap]::new(5,6)
    $p.CustomEndCap=$cap; $g.DrawLine($p,$x1,$y1,$x2,$y2)
    $p.Dispose(); $cap.Dispose()
}
Txt 'Tower property: average in stages, or directly' 750 20 32
Txt 'Pick one of these 10 pupils uniformly. X = score; G = grade; C = class.' 750 85 20
$xs=@(195,555,945,1305)
$vals=@('2, 4','6, 8, 10, 12','14, 16','18, 20')
$means=@(3,9,15,19)
for($i=0;$i -lt 4;$i++) {
    $c=if($i -lt 2){'#286aab'}else{'#168276'}
    Box $vals[$i] $xs[$i] 165 280 $c
    Arr $xs[$i] 245 $xs[$i] 340
    Box ('Class mean = '+$means[$i]) $xs[$i] 345 280 $c
}
Txt 'Average within each class' 750 278 18
Arr 195 425 375 540; Arr 555 425 375 540
Arr 945 425 1125 540; Arr 1305 425 1125 540
Txt '2/6' 240 472 19; Txt '4/6' 510 472 19
Txt '2/4' 990 472 19; Txt '2/4' 1260 472 19
Box 'Grade A mean = 7' 375 545 500 '#286aab'
Box 'Grade B mean = 17' 1125 545 500 '#168276'
Txt 'Direct: (2+4+6+8+10+12)/6 = 7;   (14+16+18+20)/4 = 17' 750 655 21
$b.Save((Join-Path $PSScriptRoot 'tower-property.png'),[System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $b.Dispose()
