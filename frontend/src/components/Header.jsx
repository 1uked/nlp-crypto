import React from "react";
import { Box, Typography } from "@mui/material";

const Header = () => {
    return (
        <Box
            sx={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "10vh",
            }}
        >
            <Typography variant="h3" component="h1" fontFamily="Roboto, sans-serif" fontWeight="bold" >
                What can I help with?
            </Typography>
        </Box>
    );
};

export default Header;
