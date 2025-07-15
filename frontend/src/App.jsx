import './App.css';
import UploadForm from './components/UploadForm';
import TrainPanel from './components/TrainPanel';
import ChatBox from './components/ChatBox';
import TrainingProgress from './components/TraningProgress';

function App() {
  return (
    <div className="container">
      <h1>🧠 LLM Fine-Tuning Playground</h1>
      <UploadForm />
      <TrainPanel />
      <TrainingProgress />
      <ChatBox />
    </div>
  );
}

export default App;