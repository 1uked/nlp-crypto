import React, { useState } from "react";
import { Paper, TextField, IconButton } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";

const PromptBar = ({ onSubmitPrompt }) => {
    const [prompt, setPrompt] = useState("");

    const handleChange = (e) => {
        setPrompt(e.target.value);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (prompt.trim() === "") return;
        if (onSubmitPrompt) {
            onSubmitPrompt(prompt);
        }
        setPrompt("");
    };

    return (
        <Paper
            component="form"
            onSubmit={handleSubmit}
            elevation={3}
            sx={{
                display: "flex",
                alignItems: "center",
                padding: "20px",
                margin: "auto",
                backgroundColor: "#222831",
                borderRadius: "25px",
                width: "50%",
            }}
        >
            {/* Text Input */}
            <TextField
                fullWidth
                placeholder="Send a message..."
                variant="standard"
                value={prompt}
                onChange={handleChange}
                InputProps={{
                    disableUnderline: true,
                    sx: {
                        color: "#fff",
                        backgroundColor: "#393E46",
                        borderRadius: "20px",
                        padding: "10px 15px",
                        fontWeight:"bold",
                    },
                }}
                sx={{ marginLeft: 1, flex: 1 }}
            />

            {/* Floating Send Button */}
            <IconButton
                type="submit"
                sx={{
                    backgroundColor: "#00ADB5",
                    color: "#000",
                    marginLeft: "10px",
                    borderRadius: "50%",
                    "&:hover": {
                        backgroundColor: "#393E46",
                        color: "#00ADB5",
                    },
                }}
            >
                <SendIcon />
            </IconButton>
        </Paper>
    );
};

export default PromptBar;
