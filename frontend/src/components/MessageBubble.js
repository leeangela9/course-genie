import RadioMenu from "./RadioMenu";

export default function MessageBubble(props) {
  const msg = props.msg;
  const formatRecs = () => {
    switch (msg.style) {
      case 1:
        return (
          <div className="recs-container">
            <p>I would recommend the following courses:</p>
            {msg.text.map((crs, i) => (
              <p key={i}>
                <strong>[{crs.code}]</strong> {crs.explanation}
              </p>
            ))}
          </div>
        );

      case 2:
        return (
          <p>
            <strong>
              [{msg.text.code}]: {msg.text.name}
            </strong>
            ({msg.text.credits} credits)
            <br />
            <br />
            <strong>Description:</strong>
            <br />
            {msg.text.description}
            <br />
            <br />
            <strong>Sentiment: </strong>
            <em>{msg.text.sentiment}</em>
            <br />
            {msg.text.summary}
          </p>
        );

      default:
        return <p>Unknown message style</p>;
    }
  };

  return (
    <div className={`msg-bub ${msg.sender === "bot" ? "left" : "right"}`}>
      <h6>{msg.sender}</h6>
      <div>
        {msg.style ? formatRecs() : <p>{msg.text}</p>}
        {msg.menu && <RadioMenu setOption={props.setOption} />}
      </div>
    </div>
  );
}
