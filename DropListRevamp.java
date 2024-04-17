// Replace the action listener for the dropdown
tokenDropdown.addActionListener(e -> {
    try {
        // Get the selected item from the dropdown
        String selectedOption = (String) tokenDropdown.getSelectedItem();
        String jwtToken;
        // Check the selected option and set the JWT token accordingly
        if ("Get UAT Token".equals(selectedOption)) {
            jwtToken = authenticateWithCertificate("www.uat.token.com");
        } else if ("Get PROD Token".equals(selectedOption)) {
            jwtToken = authenticateWithCertificate("www.prod.token.com");
        } else {
            throw new RuntimeException("Unknown token option selected");
        }
        // Set the password field with the retrieved token
        passwordField.setText(jwtToken);
    } catch (Exception ex) {
        // Handle exception during certificate authentication
        log.error("Error Authenticating with certificate!", ex);
        throw new RuntimeException(new CredentialsResolvingException("Error while resolving credentials: " + ex.getMessage(), ex));
    }
});

// Update the authenticateWithCertificate method to accept the tokenUrl
public String authenticateWithCertificate(String tokenUrl) throws Exception {
    try {
        // Initialize a new URL based on the tokenUrl
        URL url = new URL(tokenUrl);
        // Implement your authentication logic here using the URL
        // For example:
        // HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        // connection.setRequestMethod("GET");
        // int responseCode = connection.getResponseCode();
        // ...
        // Return the token or do further processing based on the response
        return tokenUrl;
    } catch (MalformedURLException e) {
        throw new RuntimeException("Invalid URL: " + tokenUrl, e);
    }
}


public String authenticateWithCertificate(String env) throws Exception {
    String tokenUrl;
    if ("Get UAT Token".equals(env)) {
        tokenUrl = "www.uat.token.com";
    } else if ("Get PROD Token".equals(env)) {
        tokenUrl = "www.prod.token.com";
    } else {
        throw new RuntimeException("Unknown environment");
    }
    
    try {
        // Initialize a new URL based on the tokenUrl
        URL url = new URL(tokenUrl);
        // Implement your authentication logic here using the URL
        // For example:
        // HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        // connection.setRequestMethod("GET");
        // int responseCode = connection.getResponseCode();
        // ...
        // Return the token or do further processing based on the response
        return tokenUrl;
    } catch (MalformedURLException e) {
        throw new RuntimeException("Invalid URL: " + tokenUrl, e);
    }
}

