import { useEffect, useState } from "react";
import Hashtag from "./hashtag";
import { Tweet } from "react-twitter-widgets";
export default function TweetViewer({ socket, topic, scope }) {
  const [messages, setMessages] = useState({data:[]});
  const [message, setMessage] = useState("");
  const [buttonStatus, setButtonStatus] = useState(false);
  const [birds, setBird] = useState([]);
  const [hashtags, setHashtags] = useState({});





  const handleClick = () => {
    if (buttonStatus === false) {
      setButtonStatus(true);
    } else {
      setButtonStatus(false);
    }
  };
  useEffect(() => {
    if (buttonStatus === true) {
      socket.emit('givedata', 'for the love of god give me some data');
      console.log('emitted')
    }
    console.log('changed')
    
    socket.on(`tweets`, (data2) => {
      setMessages({data: data2.data});
      setButtonStatus(false);
    });
  }, [socket, messages, buttonStatus, hashtags
  ]);
  
  return (
    <div className="section">
      <h3>Explicit Tweets</h3>
      <div>
          {!buttonStatus ? (
            <button onClick={handleClick}>Grab data</button>
          ) : (
            <>
              <button onClick={handleClick}>Disconnect</button>
            </>
          )}
        </div>
      <div className="info">
        <div className="section_child1">
            <p>Day View</p>
        </div>
        <div className="section_child2">
        <ul>
            {messages.data.map((message, ind) => {
              return (<li value={ind} data-count={message.color}>
                <p>
                  {message.text}
                </p>
                <p>
                  {message.count}
                </p>
              </li>)
            })}
        </ul>
        </div>
        <div className="section_child3">
          <Tweet tweetId="1597672752357380096" />
          <Tweet tweetId="1597902975002738688" />
          <Tweet tweetId="1597903161184120833" />
          <Tweet tweetId="1597903959334998018" />
          <Tweet tweetId="1597903997465427970" />
          <Tweet tweetId="841418541026877441" />
        </div>
      </div>
    </div>
  );
}