// src/components/TrainingProgress.jsx
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function TrainingProgress() {
    const [status, setStatus] = useState(null);

    useEffect(() => {
        const interval = setInterval(() => {
            axios.get('http://localhost:5000/train/status')
                .then(res => setStatus(res.data))
                .catch(err => console.error(err));
        }, 2000); // poll every 2 sec

        return () => clearInterval(interval);
    }, []);

    if (!status || status.status === 'idle') return null;

    const percent = Math.round((status.current_step / status.total_steps) * 100);

    return (
        <div>
            <h3>⏳ Training Progress</h3>
            <div style={{ background: '#ddd', height: '20px', width: '100%', borderRadius: '5px' }}>
                <div style={{
                    background: '#4caf50',
                    width: `${percent}%`,
                    height: '100%',
                    borderRadius: '5px'
                }} />
            </div>
            <p>{status.message}</p>
        </div>
    );
}
