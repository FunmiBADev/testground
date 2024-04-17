
package org.kdb.inside.brains.credentials;

import lombok.extern.slf4j.Slf4j;
import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialsError;
import org.kdb.inside.brains.core.credentials.CredentialsResolvingException;

import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Slf4j
public class UsernameCredentialsEditorRevamp extends CredentialEditor {
    private static final Logger log = LoggerFactory.getLogger(UsernameCredentialsEditorRevamp.class);
    private final JTextField usernameField = new JTextField();
    private final JButton tokenButton = new JButton();
    private final JPasswordField passwordField = new JPasswordField();
    private final String jwtToken = null; // Store the JWT token here

    public UsernameCredentialsEditorRevamp() {

        final JPanel panel = new JPanel(new GridBagLayout());

        final GridBagConstraints cons = new GridBagConstraints();
        cons.insets = new Insets(3, 3, 3, 3);
        cons.fill = GridBagConstraints.HORIZONTAL;

        addField(panel, cons, "Username", usernameField);
        addField(panel, cons, "Password", passwordField);  cons.gridx = 0;

        cons.gridy += 1;
        cons.weightx = 0;
        panel.add(new JLabel("Token"), cons);

        cons.gridx = 1;
        cons.weightx = 1;
        panel.add(tokenButton, cons);

        tokenButton.setText("Get Token");

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
        passwordField.getDocument().addDocumentListener(documentListener);

// Implement action listener for the button to
        tokenButton.addActionListener(e -> {
            try {
                String jwtToken = authenticateWithCertificate();
                // Set the password field with the retrieved token
                passwordField.setText(jwtToken);
            } catch (Exception ex) {
                // Handle exception during certificate authentication
                log.error("Error Authenticating with certificate!", ex);
                throw new RuntimeException(new CredentialsResolvingException("Error while resolving credentials: " + ex.getMessage(), ex));
            }
        });


        setLayout(new BorderLayout());
        add(panel, BorderLayout.NORTH);
    }

    public String authenticateWithCertificate() throws Exception {
        // Implement your authentication logic here
        return jwtToken;
    }

    @Override
    public String getCredentials() {
        if (passwordField.getPassword().length == 0) {
            return usernameField.getText();
        }

        return UsernameCredentialsProviderRevamp.join(usernameField.getText(), new String(passwordField.getPassword()));
    }

    @Override
    public String getViewableCredentials() {
        if (passwordField.getPassword().length == 0) {
            return usernameField.getText();
        }
        return usernameField.getText() + ":*****";
    }

    @Override
    public void setCredentials(String credentials) {
        usernameField.setText("");
        passwordField.setText("");

        if (credentials == null) {
            return;
        }

        final int i = credentials.indexOf(':');
        if (i >= 0) {
            usernameField.setText(credentials.substring(0, i));
            passwordField.setText(credentials.substring(i + 1));
        } else {
            usernameField.setText(credentials);
        }
    }

    @Override
    public List<CredentialsError> validateEditor() {
        return null;
    }

    private void addField(JPanel panel, GridBagConstraints cons, String caption, JComponent comp) {
        cons.gridx = 0;
        cons.gridy += 1;
        cons.weightx = 0;

        final JLabel l = new JLabel(caption);
        l.setLabelFor(comp);
        panel.add(l, cons);

        cons.gridx = 1;
        cons.weightx = 1;
        panel.add(comp, cons);
    }

}
