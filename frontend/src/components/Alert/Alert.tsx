type AlertProps = {
  type: "success" | "error" | "warning";
  message: string;
};

export function Alert({ type, message }: AlertProps) {
  return (
    <div className={`alert alert-${type}`}>
      {message}
    </div>
  );
}
