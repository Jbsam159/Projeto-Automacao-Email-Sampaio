import { useState } from "react";

interface EmailSelectProps {
  value: string;
  onChange: (value: string) => void;
  options: string[];
}

const EmailSelect = ({ value, onChange, options }: EmailSelectProps) => {
  const [open, setOpen] = useState(false);

  const filteredOptions = options.filter((email) =>
    email.toLowerCase().includes(value.toLowerCase())
  );

  return (
    <div className="email-select">
      <input
        type="email"
        placeholder="Email do cliente"
        value={value}
        onChange={(e) => {
          onChange(e.target.value);
          setOpen(true);
        }}
        onFocus={() => setOpen(true)}
        onBlur={() => setTimeout(() => setOpen(false), 150)}
        required
      />

      {open && filteredOptions.length > 0 && (
        <ul className="email-select-list">
          {filteredOptions.map((email) => (
            <li
              key={email}
              onClick={() => {
                onChange(email);
                setOpen(false);
              }}
            >
              {email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default EmailSelect;
