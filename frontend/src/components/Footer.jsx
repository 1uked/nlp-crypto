import React from "react";
import { Box, Link } from "@mui/material";
import GithubIcon from "@mui/icons-material/GitHub";
import LinkedInIcon from "@mui/icons-material/LinkedIn";

const Footer = () => {
    return (
        <Box
            sx={{
                alignItems: "center",
                padding: "20px",
                margin: "auto",
                borderRadius: "25px",
                bottom: 0,
                left: "50%",
            }}
        >
            <Link href="https://github.com/1uked" sx={{ mx: 1, color: "#222831" }}>
                <GithubIcon />
            </Link>
            <Link href="https://www.linkedin.com/in/luke-edwards01" sx={{ mx: 1, color: "#222831"}}>
                <LinkedInIcon />
            </Link>
        </Box>
    );
};

export default Footer;
