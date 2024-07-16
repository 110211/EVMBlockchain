@echo off
echo Starting Ganache...
start /B ganache-cli --db ./ganache-db --deterministic

REM Đợi Ganache khởi động (thời gian có thể thay đổi nếu cần)
timeout /T 5

echo Running interact.js...
cd D:\BlockChain\BE
if exist interact.js (
    echo Found interact.js, running script...
    node interact.js
) else (
    echo Error: interact.js not found in the current directory.
)
pause
