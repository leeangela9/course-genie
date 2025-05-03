import ChatWindow from "./ChatWindow";
import ChatInput from "./ChatInput";
import "../stylesheets/chat.css";
import { useState, useEffect } from "react";
import axios from "axios";
import Home from "./Home";

export default function ChatContainer(props) {
  const student = props.user;

  const mainMsg = {
    text: `Hi ${student["name"]}, how can I help you?`,
    menu: true, // refers to radio menu
    sender: "bot",
  };

  const [botTurn, setBotTurn] = useState(false);
  const [messages, setMessages] = useState([mainMsg]);
  const [option, setOption] = useState(null);
  const [needsInput, setNeedsInput] = useState(false); // refers to the need of text input
  const [userInput, setUserInput] = useState(""); // the value of the input
  const [quit, setQuit] = useState(false);

  useEffect(() => {
    console.log("new msg: ", messages[messages.length - 1]);
  }, [messages]);

  useEffect(() => {
    console.log("bot's turn? ", botTurn);
  }, [botTurn]);

  const addMsg = (msg, menu = true, sender = "bot", style = 0) => {
    setMessages((prev) => [
      ...prev,
      {
        text: msg,
        menu: menu,
        sender: sender,
        style: style,
      },
    ]);
  };

  useEffect(() => {
    if (needsInput) {
      const radios = document.querySelectorAll('input[type="radio"]');
      if (radios) {
        radios.forEach((radio) => {
          radio.disabled = true;
        });
      }
      const okBtn = document.getElementById("ok-btn");
      if (okBtn) {
        okBtn.classList.add("radio-disabled");
        okBtn.removeAttribute("id");
      }
    }
  }, [needsInput]);

  useEffect(() => {
    switch (option) {
      case "0": // bot provides menu
        addMsg(mainMsg.text);
        setBotTurn(false);
        break;
      case "1": // user triggers rec crs
        setBotTurn(true);
        getRecs();
        break;
      case "2": // user triggers crs review -> get user input
        // setBotTurn(true);
        addMsg("Please enter the course code (e.g. CSE320)", false);
        setNeedsInput(true);
        break;
      case "3": // user gave input
        setNeedsInput(false);
        getCrsReview();
        break;
      case "4":
        setQuit(true);
        break;
      case "5": // user triggers modify interests -> get user input
        addMsg("Enter your new interests", false);
        setNeedsInput(true);
        break;
      case "6": // user gave input
        setNeedsInput(false);
        changeInterests();
        break;
      case "7":
        addMsg("Enter course", false);
        setNeedsInput(true);
        break;
      case "8":
        setNeedsInput(false);
        addCCRecords();
        break;
      default:
        break;
    }
  }, [option]);

  const getRecs = async () => {
    try {
      const res = await axios.post(
        "http://localhost:8000/api/recommendations",
        { id: student["id"] }
      );
      console.log(res.data);
      addMsg(res.data, false, "bot", 1);
    } catch (error) {
      const err = "Error posting recommendation request: " + error;
      addMsg(err, false);
    } finally {
      setOption("0");
    }
  };

  const getCrsReview = async () => {
    try {
      const res = await axios.get(
        `http://localhost:8000/api/courses/${userInput.replace(" ", "")}`
      );
      console.log(res.data);
      addMsg(res.data, false, "bot", 2);
    } catch (error) {
      const err = "Error posting recommendation request: " + error;
      console.log(err);
      addMsg("Invalid code.", false);
    } finally {
      setUserInput("");
      setOption("0");
    }
  };

  const changeInterests = async () => {
    try {
      const res = await axios.post("http://localhost:8000/api/edit_interests", {
        student_id: student["id"],
        interests: userInput,
      });
      if (res.status === 200) {
        addMsg("Succesfully modified", false);
      } else {
        addMsg("Failed to modify", false);
      }
    } catch (error) {
      const err = "Error posting recommendation request: " + error;
      console.log(err);
      addMsg(err, false);
    } finally {
      setUserInput("");
      setOption("0");
    }
  };

  const addCCRecords = async () => {
    try {
      const res = await axios.post("http://localhost:8000/api/add_cc_record", {
        student_id: student["id"],
        course_id: userInput,
      });
      if (res.status === 200) {
        addMsg("Succesfully inserted", false);
      } else {
        addMsg("Failed to insert", false);
      }
    } catch (error) {
      const err = "Error posting recommendation request: " + error;
      console.log(err);
      addMsg(err, false);
    } finally {
      setUserInput("");
      setOption("0");
    }
  };

  return quit ? (
    <Home />
  ) : (
    <div className="chat-container">
      <h1 className="chat-header">SBU Course Recommender</h1>
      <ChatWindow messages={messages} setOption={setOption} student={student} />
      {needsInput && (
        <ChatInput
          setNeedsInput={setNeedsInput}
          addMsg={addMsg}
          student={student}
          option={option}
          setOption={setOption}
          setUserInput={setUserInput}
        />
      )}
    </div>
  );
}
