const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const multer = require('multer');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

// '/run/voice' 엔드포인트에 대한 요청을 처리
app.post('/run/voice', (req, res) => {
    console.log('Received request on /run/voice');

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
        res.send({ message: 'Voice.py script executed successfully', code });
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
