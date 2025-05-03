import { useState } from "react";

export default function RadioMenu(props) {
  const [value, setValue] = useState("");
  const [isDisabled, setIsDisabled] = useState(false);

  const submit = () => {
    if (!value || isDisabled) return;
    console.log("triggered");

    props.setOption(value);
    setIsDisabled(true);
  };

  return (
    <div className="radio-input">
      <p>Select a menu:</p>
      <form>
        <label>
          <div>
            <input
              type="radio"
              name="choice"
              value="1"
              onChange={(e) => setValue(e.target.value)}
              checked={value === "1"}
              disabled={isDisabled}
            />
            Recommend courses
          </div>
        </label>

        <label>
          <input
            type="radio"
            name="choice"
            value="2"
            onChange={(e) => setValue(e.target.value)}
            checked={value === "2"}
            disabled={isDisabled}
          />
          Review a course
        </label>

        <label>
          <input
            type="radio"
            name="choice"
            value="5"
            onChange={(e) => setValue(e.target.value)}
            checked={value === "5"}
            disabled={isDisabled}
          />
          Modify interest(s)
        </label>

        <label>
          <input
            type="radio"
            name="choice"
            value="4"
            onChange={(e) => setValue(e.target.value)}
            checked={value === "4"}
            disabled={isDisabled}
          />
          Quit
        </label>
      </form>

      <div
        id="ok-btn"
        className={`radio-btn ${isDisabled ? "radio-disabled" : ""}`}
        onClick={isDisabled ? null : submit}
      >
        Ok
      </div>
    </div>
  );
}
