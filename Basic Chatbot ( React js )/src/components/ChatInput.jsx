import { useState } from "react";
import { Chatbot } from "supersimpledev";
import './ChatInput.css'

export function ChatInput({ messages, setmessages }) {
  const [textInput, setTextInput] = useState("");

  function saveTextInput(event) {
    setTextInput(event.target.value);
  }

  const handleKeyDown = (event) => {
    if (event.key === "Enter") {
      sendMessage()
    }
  };

  function sendMessage() {
    const newChatMessages = [
      ...messages,
      { message: textInput, sender: "user", id: crypto.randomUUID() },
    ];
    setmessages(newChatMessages);
    const response = Chatbot.getResponse(textInput);
    setmessages([
      ...newChatMessages,
      { message: response, sender: "robot", id: crypto.randomUUID() },
    ]);
    setTextInput("");
  }

  return (
    <div className="upper">
      <input
        placeholder="Send Message To Chatbot"
        size="30"
        onChange={saveTextInput}
        onKeyDown={handleKeyDown}
        value={textInput}
        className="text-input"
      />
      <button onClick={sendMessage} className="btn">
        Send
      </button>
    </div>
  );
}