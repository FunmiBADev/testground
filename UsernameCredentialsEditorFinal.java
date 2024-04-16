package org.kdb.inside.brains.credentials;

import lombok.extern.slf4j.Slf4j;
import org.kdb.inside.brains.core.credentials.CredentialEditor;
import org.kdb.inside.brains.core.credentials.CredentialsError;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.*;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import java.awt.*;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.util.List;

//Update test to take into consideration that the these properties are private and in accessible outside of the UsernameCredentialsEditor Class
//private final JTextField usernameField = new JTextField();
//private final JButton tokenButton = new JButton(); // Changed JBPasswordField to JButton
//private String jwtToken = null; // Store the JWT token here

@Slf4j
public class UsernameCredentialsEditor extends CredentialEditor {
    private final JTextField usernameField = new JTextField();
    private final JButton tokenButton = new JButton(); // Changed JBPasswordField to JButton
    private String jwtToken = null; // Store the JWT token here

    public UsernameCredentialsEditor() {

        final JPanel panel = new JPanel(new GridBagLayout());

        final GridBagConstraints cons = new GridBagConstraints();
        cons.insets = new Insets(3, 3, 3, 3);
        cons.fill = GridBagConstraints.HORIZONTAL;

        addField(panel, cons, "Username", usernameField);
        addField(panel, cons, "Token", tokenButton);

        tokenButton.setText("Get Token");

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

        tokenButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    jwtToken = authenticateWithCertificate();
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

        setLayout(new BorderLayout());
        add(panel, BorderLayout.NORTH);
    }

    public String authenticateWithCertificate() throws Exception {
        // Implement your authentication logic here
        return "your_jwt_token";
    }

    @Override
    public String getCredentials() {
//        return SystemVarCredentialsProvider.join(usernameField.getText(), (String) varnameField.getSelectedItem());
        if (jwtToken != null && !jwtToken.isEmpty()) {
            return usernameField.getText() + ":" + jwtToken;
        } else {
            return null;
        }
    }

    @Override
    public String getViewableCredentials() {
        return getCredentials();
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

//        tokenButton.addActionListener(new ActionListener() {
//        @Override
//        public void actionPerformed(ActionEvent e) {
//            try {
//                jwtToken = authenticateWithCertificate();
//                // Here you can handle the retrieved jwtToken, maybe update UI or store it somewhere
//                // Update the displayed value accordingly
//                setCredentials(getCredentials()); // Set credentials to refresh the displayed passwordField
//            } catch (Exception ex) {
//                ex.printStackTrace(); // Handle the exception appropriately
//            }
//        }
//    });
