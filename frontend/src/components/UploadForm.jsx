// src/components/UploadForm.jsx
import { useState } from 'react';
import axios from 'axios';

export default function UploadForm() {
    const [file, setFile] = useState(null);

    const handleUpload = async () => {
        if (!file) return;
        const formData = new FormData();
        formData.append('file', file);
        const res = await axios.post('http://localhost:5000/upload', formData);
        localStorage.setItem('dataset_path', res.data.path);
        alert('Upload successful!');
    };

    return (
        <div>
            <h2>📂 Upload Dataset</h2>
            <input type="file" onChange={(e) => setFile(e.target.files[0])} />
            <button onClick={handleUpload}>Upload</button>
        </div>
    );
}
