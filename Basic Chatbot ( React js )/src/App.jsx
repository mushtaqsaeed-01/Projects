import { useState } from 'react';
import { ChatInput } from './components/ChatInput';
import { ChatMessages } from './components/ChatMessages';
import './App.css'

function App() {
  const [inputState, setInputState] = useState("down");
  const [chatMessages, setchatMessages] = useState([]);

  return (
    <div className="main">
      {inputState === "down" && (<button className="btn-input" onClick={() => { setInputState("up"); }}>
        {" "}
          Top Input
        {" "}
        </button>
      )}
      {inputState === "down" && <ChatMessages messages={chatMessages} />}
      <ChatInput messages={chatMessages} setmessages={setchatMessages} />
      {inputState === "up" && <ChatMessages messages={chatMessages} />}
      {inputState === "up" && (<button className="btn-input" onClick={() => { setInputState("down") }}>
        {" "}
          Bottom Input
        {" "}
        </button>
      )}
    </div>
  );
}

export default App
