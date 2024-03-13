import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialsError;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class SystemVarCredentialsEditor extends CredentialEditor {
    private final JTextField usernameField = new JTextField();
    private final JPasswordField passwordField = new JPasswordField(); // Changed field
    // Timer for tracking inactivity
    private Timer inactivityTimer;
    private static final long INACTIVITY_TIMEOUT = 120000; // 2 minutes in milliseconds

    public SystemVarCredentialsEditor() {
        final JPanel p = new JPanel(new GridBagLayout());
        final GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(3, 3, 3, 3);
        c.fill = GridBagConstraints.HORIZONTAL;

        addField(p, c, "Username", usernameField);
        addField(p, c, "Password", passwordField); // Updated field

        // Start the inactivity timer when any field changes
        usernameField.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                resetInactivityTimer();
                processCredentialChanged(getCredentials());
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                resetInactivityTimer();
                processCredentialChanged(getCredentials());
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                resetInactivityTimer();
                processCredentialChanged(getCredentials());
            }
        });

        passwordField.getDocument().addDocumentListener(new DocumentListener() { // Added for password field
            @Override
            public void insertUpdate(DocumentEvent e) {
                resetInactivityTimer();
                processCredentialChanged(getCredentials());
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                resetInactivityTimer();
                processCredentialChanged(getCredentials());
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                resetInactivityTimer();
                processCredentialChanged(getCredentials());
            }
        });

        setLayout(new BorderLayout());
        add(p, BorderLayout.NORTH);
    }

    @Override
    public String getCredentials() {
        return SystemVarCredentialsProvider.join(usernameField.getText(), new String(passwordField.getPassword())); // Updated to retrieve password
    }

    @Override
    public String getViewableCredentials() {
        return getCredentials();
    }

    @Override
    public void setCredentials(String credentials) {
        final String[] split = credentials.split(":");
        if (split.length > 0) {
            usernameField.setText(split[0]);
        }
        if (split.length > 1) {
            passwordField.setText(split[1]); // Updated to set password
        }
    }

    @Override
    public List<CredentialsError> validateEditor() {
        List<CredentialsError> res = new ArrayList<>();
        if (usernameField.getText().isBlank()) {
            res.add(new CredentialsError("Username can't be empty", usernameField));
        }

        // Checking for password blankness
        if (new String(passwordField.getPassword()).isBlank()) {
            res.add(new CredentialsError("Password can't be empty", passwordField));
        }

        return res;
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

    // Reset the inactivity timer
    private void resetInactivityTimer() {
        if (inactivityTimer != null) {
            inactivityTimer.cancel();
        }
        inactivityTimer = new Timer();
        inactivityTimer.schedule(new TimerTask() {
            @Override
            public void run() {
                // Disconnect database connection here
                System.out.println("Disconnecting database connection due to inactivity...");
                // You should add your disconnection logic here
            }
        }, INACTIVITY_TIMEOUT);
    }
}
