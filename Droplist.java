// Replace the JButton declaration with a JComboBox
private final JComboBox<String> tokenDropdown = new JComboBox<>(new String[]{"Get UAT Token", "Get PROD Token"});

// Replace the tokenButton setup with the tokenDropdown
panel.add(tokenDropdown, cons);

// Replace the action listener for the dropdown
tokenDropdown.addActionListener(e -> {
    try {
        // Get the selected item from the dropdown
        String selectedOption = (String) tokenDropdown.getSelectedItem();
        String jwtToken;
        // Check the selected option and set the JWT token accordingly
        if ("Get UAT Token".equals(selectedOption)) {
            jwtToken = authenticateWithCertificate("UAT");
        } else if ("Get PROD Token".equals(selectedOption)) {
            jwtToken = authenticateWithCertificate("PROP");
        } else {
            throw new RuntimeException("Invalid token option selected");
        }
        // Set the password field with the retrieved token
        passwordField.setText(jwtToken);
    } catch (Exception ex) {
        // Handle exception during certificate authentication
        log.error("Error Authenticating with certificate!", ex);
        throw new RuntimeException(new CredentialsResolvingException("Error while resolving credentials: " + ex.getMessage(), ex));
    }
});

// Update the authenticateWithCertificate method to accept an environment parameter
public String authenticateWithCertificate(String env) throws Exception {
    // Implement your authentication logic here based on the environment
    return getUrl(env);
}
