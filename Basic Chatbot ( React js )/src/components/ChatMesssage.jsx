import "./ChatMesssage.css";

export function ChatMesssage({ message, sender }) {
  //                    |        |
  //                   same as below
  //
  // const message = props.message;
  // const sender = props.sender;

  // const { message, sender } = props;

  /*
            if (sender === "robot"){
                return (
                    <div>
                        <img src="images/robot.png" width="50" />
                        {message}
                    </div>
                )
            }
            */

  return (
    <div className={sender === "user" ? "user-message" : "robot-message"}>
      {sender === "robot" && (
        <img src="src/assets/robot.png" width="50" height="50" />
      )}
      <div className="text">{message}</div>
      {sender === "user" && (
        <img src="src/assets/user.png" width="50" height="50" />
      )}
    </div>
  );
}