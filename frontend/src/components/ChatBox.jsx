// src/components/ChatBox.jsx
import { useState } from 'react';
import axios from 'axios';

export default function ChatBox() {
    const [prompt, setPrompt] = useState('');
    const [response, setResponse] = useState('');

    const handleChat = async () => {
        const model_path = localStorage.getItem('model_path');
        const res = await axios.post('http://localhost:5000/chat', {
            model_path,
            prompt
        });
        setResponse(res.data.response);
    };

    return (
        <div>
            <h2>💬 Chat With Your Fine-Tuned Model</h2>
            <textarea
                placeholder="Enter prompt here..."
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows={3}
                cols={50}
            />
            <br />
            <button onClick={handleChat}>Send</button>
            <pre>{response}</pre>
        </div>
    );
}
