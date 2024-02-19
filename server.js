const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

app.post('/run/voice', (req, res) => {
    // Voice.py 파이썬 스크립트 실행
    const pythonProcess = spawn('python', ['./Voice.py']);

    pythonProcess.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
        // 파이썬 스크립트 실행 완료 후 클라이언트에 응답 전송
        res.send({ message: 'Voice.py script executed successfully', code });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
