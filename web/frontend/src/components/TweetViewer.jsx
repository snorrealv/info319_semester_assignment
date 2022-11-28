import { useEffect, useState } from "react";

export default function TweetViewer({ socket, topic, scope }) {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);

  const handleText = (e) => {
    const inputMessage = e.target.value;
    setMessage(inputMessage);
  };
  console.log(`tweet_view_${topic}_${scope}`)
  useEffect(() => {
    socket.on(`tweet_view_${topic}_${scope}`, (data) => {
      
      console.log('data', data.data)
      setMessages([...messages, data.data]);
      
    });
  }, [socket, messages]);

  return (
    <div>
      <h2>This is supposed to be a cool thing</h2>
      <ul>
        {messages.map((message, ind) => {
          return <li key={ind}>{message}</li>;
        })}
      </ul>
    </div>
  );
}