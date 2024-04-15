import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public static class UsernameCredentialsEditor extends CredentialEditor {
    final JBTextField usernameField = new JBTextField();
    final JButton getJwtTokenButton = new JButton(); // Changed JBPasswordField to JButton
    String jwtToken = null; // Store the JWT token here

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

        add(new JLabel("Token:"), c.nextLine().next());
        add(getJwtTokenButton, c.nextLine().next(). colspan(2)); // Changed to JButton

        getJwtTokenButton.setText("Get JWT Token");

        // Action listener for the getJwtTokenButton
        getJwtTokenButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    jwtToken = authenticateWithCertificate();
                    // Here you can handle the retrieved jwtToken, maybe update UI or store it somewhere
                    // Update the displayed value accordingly
                    setCredentials(getCredentials()); // Set credentials to refresh the displayed passwordField
                } catch (Exception ex) {
                    ex.printStackTrace(); // Handle the exception appropriately
                }
            }
        });

        final DocumentListener documentListener = new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent documentEvent) {
                processCredentialChanged(getCredentials());
            }

            @Override
            public void removeUpdate(DocumentEvent documentEvent) {
                processCredentialChanged(getCredentials());
            }

            @Override
            public void changedUpdate(DocumentEvent documentEvent) {
                processCredentialChanged(getCredentials());
            }
        };

        usernameField.getDocument().addDocumentListener(documentListener);
    }

    public String authenticateWithCertificate() throws Exception {
        // Implement your authentication logic here
        return "your_jwt_token";
    }

    @Override
    public String getCredentials() {
        if (jwtToken != null) {
            return usernameField.getText() + ":" + jwtToken;
        } else {
            return usernameField.getText();
        }
    }

    @Override
    public String getViewableCredentials() {
        if (jwtToken != null) {
            return usernameField.getText() + ":*****";
        } else {
            return usernameField.getText();
        }
    }

    @Override
    public void setCredentials(String credentials) {
        usernameField.setText("");
        // Do not set passwordField directly, as it's not used anymore
        // Instead, update jwtToken and let getCredentials() handle the display
        jwtToken = null; // Reset the JWT token when setting new credentials
        if (credentials == null) {
            return;
        }
        final int i = credentials.indexOf(':');
        if (i >= 0) {
            usernameField.setText(credentials.substring(0, i));
            jwtToken = credentials.substring(i + 1);
        } else {
            usernameField.setText(credentials);
        }
    }

    @Override
    public List<CredentialsError> validateEditor() {
        return null;
    }
}
