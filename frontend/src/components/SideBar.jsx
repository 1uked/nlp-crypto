// Sidebar.jsx
import React from "react";
import {
  Box,
  Paper,
  IconButton,
  Typography,
  List,
  ListItem,
  ListItemText,
  Button,
  ListItemSecondaryAction,
} from "@mui/material";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import DeleteIcon from "@mui/icons-material/Delete";
import elicon from "../../src/assets/elizaos-logo.png";

const Sidebar = ({ isOpen, onToggle, chatSessions, activeChatId, onSelectChat, onNewChat, onDeleteChat }) => {
  return (
    <Paper
      elevation={3}
      sx={{
        position: "fixed",
        top: 0,
        left: 0,
        bottom: 0,
        width: isOpen ? "25%" : "50px",
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

      {isOpen && (
        <Box sx={{ p: 2 }}>
          <Button variant="contained" color="primary" fullWidth onClick={onNewChat}>
            New Chat
          </Button>
          <Typography variant="h6" fontWeight="bold" sx={{ mt: 2, mb: 2 }}>
            Chats
          </Typography>
          <List>
            {chatSessions.map((session) => (
              <ListItem
                key={session.id}
                button
                selected={session.id === activeChatId}
                onClick={() => onSelectChat(session.id)}
              >
                <ListItemText primary={session.title} />
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={(e) => {
                      e.stopPropagation(); // Prevent selecting the chat when deleting.
                      onDeleteChat(session.id);
                    }}
                    sx={{ color: "#fff" }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            ))}
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
            Powered by ElizaOS
          </Typography>
        ) : (
          <IconButton>
            <img src={elicon} alt="Eliza Logo" style={{ height: "24px", marginLeft: "4px" }} />
          </IconButton>
        )}
      </Box>
    </Paper>
  );
};

export default Sidebar;
