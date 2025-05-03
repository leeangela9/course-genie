import { useEffect, useRef } from "react";
import "../stylesheets/chat.css";
import MessageBubble from "./MessageBubble";

export default function ChatWindow(props) {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [props.messages]); // triggers when messages change

  return (
    <div className="chat-window" ref={scrollRef}>
      {props.messages.map((msg, index) => (
        <MessageBubble
          key={index}
          msg={msg}
          setOption={props.setOption}
          student={props.student}
        />
      ))}
    </div>
  );
}
