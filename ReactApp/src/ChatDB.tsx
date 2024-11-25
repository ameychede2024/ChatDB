import React, { useState, useRef, useEffect } from 'react';
import FileUpload from './FileUpload';
import './ChatDB.css';

const BOT_IMG = "/chatdb.jpg";
const PERSON_IMG = "/person.png";
const BOT_NAME = "ChatDB 42";
const PERSON_NAME = "User";

const BOT_MSGS = [
  "Hi, how are you?",
  "Ohh... I can't understand what you trying to say. Sorry!",
  "I like to play games... But I don't know how to play!",
  "Sorry if my answers are not relevant. :))",
  "I feel sleepy! :(",
  "I'm sexy and I know it! ;)",
  "You're not worth it. Just Die! :(",
];

interface Message {
  name: string;
  img: string;
  side: 'left' | 'right';
  text: string;
}

const ChatDB: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const chatRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const appendMessage = (name: string, img: string, side: 'left' | 'right', text: string) => {
    setMessages(prevMessages => [...prevMessages, { name, img, side, text }]);
  };

  const botResponse = () => {
    const r = Math.floor(Math.random() * BOT_MSGS.length);
    const msgText = BOT_MSGS[r];
    const delay = msgText.split(" ").length * 100;

    setTimeout(() => {
      appendMessage(BOT_NAME, BOT_IMG, "left", msgText);
    }, delay);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText) return;

    appendMessage(PERSON_NAME, PERSON_IMG, "right", inputText);
    setInputText('');
    botResponse();
  };

  return (
    <section className="msger">
      <FileUpload
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />

      <header className="msger-header">
        <div className="msger-header-title">
          <i className="fas fa-comment-alt"></i> ChatDB 42
        </div>
        <div className="msger-header-options">
          <span>
            <i className="fas fa-cog">
              <button onClick={() => setIsModalOpen(true)}>
                Upload File
              </button>
            </i>
          </span>
        </div>
      </header>

      <main className="msger-chat" ref={chatRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`msg ${msg.side}-msg`}>
            <div className="msg-img" style={{backgroundImage: `url(${msg.img})`}}></div>
            <div className="msg-bubble">
              <div className="msg-info">
                <div className="msg-info-name">{msg.name}</div>
                <div className="msg-info-time">{new Date().toLocaleTimeString()}</div>
              </div>
              <div className="msg-text">{msg.text}</div>
            </div>
          </div>
        ))}
      </main>

      <form className="msger-inputarea" onSubmit={handleSubmit}>
        <input
          type="text"
          className="msger-input"
          placeholder="Enter your message..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button type="submit" className="msger-send-btn">Send</button>
      </form>
    </section>
  );
};

export default ChatDB;