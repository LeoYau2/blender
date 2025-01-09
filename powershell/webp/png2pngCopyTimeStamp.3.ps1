#$OutputEncoding = [console]::InputEncoding = [console]::OutputEncoding = [Text.UTF8Encoding]::UTF8
#$OutputEncoding = New-Object -typename System.Text.UTF8Encoding

$countAll = 0
$count = 0

foreach($file in Get-ChildItem -Filter *.png)
{
    $countAll++
}
echo "$countAll png files"
pause

mkdir png
foreach($file in Get-ChildItem -Filter *.png)
{
    $na = [io.path]::GetFileNameWithoutExtension("$file")
    ffmpeg -hide_banner -i "$na.png" -c:v png "png\$na.png"
    (Get-Item "png/$na.png").CreationTime=((Get-Item "$na.png").CreationTime)
    (Get-Item "png/$na.png").LastWriteTime=((Get-Item "$na.png").LastWriteTime)
    (Get-Item "png/$na.png").LastAccessTime=((Get-Item "$na.png").LastAccessTime)

    $count++
    echo -------------------------------------------------------------
    echo $na
    echo $file.FullName
    $progress = [math]::round($count / $countAll * 100,3)
    echo "$count/$countAll progress $progress%"
    echo -------------------------------------------------------------
}
(New-Object Media.SoundPlayer "C:\Windows\Media\notify.wav").Play();
pause
