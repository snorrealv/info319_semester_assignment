import { useEffect, useState } from "react";

export default function AddQuery({ socket }) {
  const [message, setMessage] = useState("");

  const handleText = (e) => {
    const inputMessage = e.target.value;
    setMessage(inputMessage);
  };

  const handleSubmit = () => {
    if (!message) {
      return;
    }
    socket.emit("query", message);
    setMessage("");
  };

  return (
    <div className="navbar_input">
      <input type="text" value={message} onChange={handleText} placeholder='Add hashtag to follow ...' />
      <button onClick={handleSubmit}>submit</button>
    </div>
  );
}