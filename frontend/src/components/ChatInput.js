import "../stylesheets/chat.css";
import { useState } from "react";

export default function ChatInput(props) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;
    props.addMsg(input, false, props.student.name);
    props.setUserInput(input);
    props.setOption(String(parseInt(props.option) + 1));
    setInput("");
  };

  return (
    <div className="chat-input">
      <input
        type="text"
        placeholder="Type your message here"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") handleSend();
        }}
      />
      <div className="send-btn" onClick={handleSend}>
        Send
      </div>
    </div>
  );
}
