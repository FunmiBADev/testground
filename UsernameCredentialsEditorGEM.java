public static class UsernameCredentialsEditor extends CredentialEditor {
  final JBTextField usernameField = new JBTextField();
  // Replaced password field with a button
  final JButton getJwtTokenButton = new JButton("Get JWT Token");

  public UsernameCredentialsEditor() {
      final GridBag c = new GridBag()
              .setDefaultAnchor(0, GridBagConstraints.LINE_START)
              .setDefaultAnchor(1, GridBagConstraints.CENTER)
              .setDefaultWeightX(1, 1)
              .setDefaultFill(GridBagConstraints.HORIZONTAL)
              .setDefaultInsets(3, 10, 3, 3);

      setLayout(new GridBagLayout());

      add(new JLabel("Username:"), c.nextLine().next());
      add(usernameField, c.next());

      // Add the button in place of the password field
      add(getJwtTokenButton, c.nextLine().next(). colspan(2));  // Spans 2 columns

      // Implement action listener for the button
      getJwtTokenButton.addActionListener(new ActionListener() {
          @Override
          public void actionPerformed(ActionEvent e) {
              try {
                  String jwtToken = authenticateWithCertificate();
                  // Handle the retrieved JWT token (e.g., display or store)
                  // ...
              } catch (Exception ex) {
                  // Handle exception during certificate authentication
                  // ...
              }
          }
        });

      // Remove the document listener as password is not collected
      // usernameField.getDocument().addDocumentListener(documentListener);  // Removed
  }

  // ... other methods remain the same (getCredentials, getViewableCredentials, setCredentials, validateEditor)
}


public UsernameCredentialsEditor() {
  // ... (other code)

  getJwtTokenButton.addActionListener(new ActionListener() {
      @Override
      public void actionPerformed(ActionEvent e) {
          try {
              String jwtToken = authenticateWithCertificate();
              // **Temporary storage example (use with caution):**
              String temporaryCredentials = usernameField.getText() + ":" + jwtToken;

              // Use the temporary credentials for current UI interaction (if needed)
              // ...

              setCredentials(temporaryCredentials); // Set credentials to refresh the displayed passwordField

              // Clear the temporary credentials after use
              temporaryCredentials = null;
          } catch (Exception ex) {
              // Handle exception during certificate authentication
              // ...
          }
      }
  });
}
