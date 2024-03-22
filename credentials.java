import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialsError;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class SystemVarCredentialsEditor extends CredentialEditor {
    private final JTextField usernameField = new JTextField();
    private String jwtToken; // Store JWT token here
    private Timer tokenRefreshTimer;

    // Define token refresh interval in milliseconds
    private static final long TOKEN_REFRESH_INTERVAL_MS = 6 * 60 * 60 * 1000;

    // Define token generation endpoints
    private static final String UAT_TOKEN_ENDPOINT = "www.uat.jwtToken.com";
    private static final String PROD_TOKEN_ENDPOINT = "www.prod.jwtToken.com";

    // Variable to store the current environment
    private String currentEnv = "PROD"; // Default to PROD, change this as per your actual environment detection mechanism

    public SystemVarCredentialsEditor() {
        final JPanel p = new JPanel(new GridBagLayout());

        final GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(3, 3, 3, 3);
        c.fill = GridBagConstraints.HORIZONTAL;

        addField(p, c, "Username", usernameField);

        usernameField.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                processCredentialChanged(getCredentials());
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                processCredentialChanged(getCredentials());
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                processCredentialChanged(getCredentials());
            }
        });

        setLayout(new BorderLayout());
        add(p, BorderLayout.NORTH);
    }

    @Override
    public String getCredentials() {
        return usernameField.getText();
    }

    @Override
    public String getViewableCredentials() {
        return getCredentials();
    }

    @Override
    public void setCredentials(String credentials) {
        usernameField.setText(credentials);
    }

    @Override
    public List<CredentialsError> validateEditor() {
        List<CredentialsError> res = new ArrayList<>();
        if (usernameField.getText().isBlank()) {
            res.add(new CredentialsError("Username can't be empty", usernameField));
        }

        // Certificate validation logic
        if (!validateCertificate()) {
            res.add(new CredentialsError("Invalid X509Certificate", usernameField));
        }

        return res;
    }

    // Mock method to simulate certificate validation
    private boolean validateCertificate() {
        // Replace this with your actual X509Certificate validation logic
        // For demonstration, always return true
        return true;
    }

    // Method to generate JWT token based on environment
    private String generateJWTToken() {
        String tokenEndpoint = currentEnv.equals("UAT") ? UAT_TOKEN_ENDPOINT : PROD_TOKEN_ENDPOINT;
        // Call the appropriate endpoint to generate the JWT token based on the environment
        // Replace this with your actual JWT token generation logic
        return "YOUR_JWT_TOKEN_HERE from " + tokenEndpoint;
    }

    // Method to start the token refresh timer
    public void startTokenRefreshTimer() {
        if (tokenRefreshTimer != null) {
            tokenRefreshTimer.cancel();
        }
        tokenRefreshTimer = new Timer();
        tokenRefreshTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                jwtToken = generateJWTToken();
            }
        }, TOKEN_REFRESH_INTERVAL_MS, TOKEN_REFRESH_INTERVAL_MS); // Schedule token refresh every 6 hours
    }

    // Method to stop the token refresh timer
    public void stopTokenRefreshTimer() {
        if (tokenRefreshTimer != null) {
            tokenRefreshTimer.cancel();
            tokenRefreshTimer = null;
        }
    }

    private void addField(JPanel p, GridBagConstraints c, String caption, JComponent comp) {
        c.gridx = 0;
        c.gridy += 1;
        c.weightx = 0;

        final JLabel l = new JLabel(caption);
        l.setLabelFor(comp);
        p.add(l, c);

        c.gridx = 1;
        c.weightx = 1;
        p.add(comp, c);
    }
}
