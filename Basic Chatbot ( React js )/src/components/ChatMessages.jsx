import { useRef, useEffect } from 'react'
import { ChatMesssage } from './ChatMesssage';
import './ChatMessages.css'

export function ChatMessages({ messages }) {
  // const arr = React.useState([{........}])
  // const chatMessages = arr[0]
  // const setchatMessages = arr[1]
  const scrollDownMessage = useRef(null);
  useEffect(() => {
    const containerElem = scrollDownMessage.current;
    containerElem.scrollTop = containerElem.scrollHeight;
  }, [messages]);

  return (
    <div className="lower" ref={scrollDownMessage}>
      {messages.map((chatmessages) => {
        return (
          <ChatMesssage
            message={chatmessages.message}
            sender={chatmessages.sender}
            key={chatmessages.id}
          />
        );
      })}
    </div>
  );
}