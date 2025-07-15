// src/components/TrainPanel.jsx
import { useState } from 'react';
import axios from 'axios';

const models = [
    'gpt2',
    'mistralai/Mistral-7B-Instruct-v0.1',
    'tiiuae/falcon-rw-1b'
];

export default function TrainPanel() {
    const [model, setModel] = useState(models[0]);

    const handleTrain = async () => {
        const dataset_path = localStorage.getItem('dataset_path');
        const res = await axios.post('http://localhost:5000/train', {
            base_model: model,
            dataset_path,
        });
        localStorage.setItem('model_path', res.data.model_path);
        alert('Training started (or finished quickly if small).');
    };

    return (
        <div>
            <h2>🧪 Fine-Tune Model</h2>
            <select value={model} onChange={(e) => setModel(e.target.value)}>
                {models.map((m, i) => (
                    <option key={i} value={m}>{m}</option>
                ))}
            </select>
            <button onClick={handleTrain}>Start Fine-Tuning</button>
        </div>
    );
}
