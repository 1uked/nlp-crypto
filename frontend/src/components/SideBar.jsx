import React from "react";
import {
    Box,
    Paper,
    IconButton,
    Typography,
    List,
    ListItem,
    ListItemText,
} from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";

const Sidebar = ({ isOpen, onToggle }) => {
    return (
        <Paper
            elevation={3}
            sx={{
                position: "fixed",
                top: 0,
                left: 0,
                bottom: 0,
                width: isOpen ? "25%" : "50px", // Adjusts width based on isOpen
                backgroundColor: "#393E46",
                color: "#fff",
                transition: "width 0.3s ease",
                overflow: "hidden",
            }}
        >
            {/* Toggle Button */}
            <Box
                sx={{
                    display: "flex",
                    justifyContent: isOpen ? "flex-end" : "center",
                    p: 1,
                }}
            >
                <IconButton
                    onClick={onToggle}
                    sx={{
                        color: "#00ADB5",
                        "&:hover": {
                            backgroundColor: "#00ADB5",
                            color: "#222831",
                        },
                    }}
                >
                    {isOpen ? <ChevronLeftIcon /> : <ChevronRightIcon />}
                </IconButton>
            </Box>

            {/* Sidebar Content */}
            {isOpen && (
                <Box sx={{ p: 2 }}>
                    <Typography variant="h6" fontWeight="bold" sx={{ mb: 2}}>
                        Chats
                    </Typography>
                    <List>
                        <ListItem button>
                            <ListItemText primary="Chat 1" />
                        </ListItem>
                        <ListItem button>
                            <ListItemText primary="Chat 2" />
                        </ListItem>
                        <ListItem button>
                            <ListItemText primary="Chat 3" />
                        </ListItem>
                    </List>
                </Box>
            )}
            <Box
                sx={{
                    position: "absolute",
                    bottom: 0,
                    width: "100%",
                    textAlign: "center",
                    paddingY: 1,
                }}
            >
                {isOpen ? (
                    <Typography variant="caption">
                        Powered by ElizaOS{" "}
                        <img
                            src="../assets/elizaos-logo.png"
                            style={{ height: "16px", marginLeft: "4px" }}
                        />
                    </Typography>
                ) : (
                    <IconButton>
                        <img
                            src="../assets/elizaos-logo.png"
                            style={{ height: "24px" }}
                        />
                    </IconButton>
                )}
            </Box>
        </Paper>
    );
};

export default Sidebar;
