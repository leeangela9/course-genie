import { useState } from "react";
import axios from "axios";

export default function Welcome(props) {
  const [input, setInput] = useState("");
  const [title, setTitle] = useState("Welcome, Student! :)");

  const handleSend = () => {
    if (input.trim() === "") return;
    verify();
  };

  const verify = async () => {
    console.log("verifying ", input, "...");
    try {
      const res = await axios.post("http://localhost:8000/api/users", {
        student_id: input,
      });

      console.log(res.data);

      if (res.status === 200) {
        props.setUser(res.data);
      }
    } catch (error) {
      setTitle("Invalid ID. Try again.");
      console.log("Error posting recommendation request:", error);
    } finally {
      setInput("");
    }
  };

  return (
    <div id="id-window">
      <h1>{title}</h1>
      <div className="chat-input">
        <input
          type="text"
          placeholder={"Enter your Student ID here"}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSend();
          }}
        />
        <div id="id-btn" onClick={handleSend}>
          Ok
        </div>
      </div>
    </div>
  );
}
