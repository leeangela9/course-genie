import { useState, useEffect } from "react";
import ChatContainer from "./ChatContainer";
import Welcome from "./Welcome";

export default function Home() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    console.log("User ID:", user?.id);
  }, [user]);

  return (
    <div className="con">
      {user ? <ChatContainer user={user} /> : <Welcome setUser={setUser} />}
    </div>
  );
}
