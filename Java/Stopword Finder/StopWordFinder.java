import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;
import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class StopWordFinder extends JFrame{
    JLabel ta_label, out_label;
    JTextArea textarea;
    JButton submit;
    JTextArea output;
    List<String> stopwords;

    StopWordFinder(){
        try{
            stopwords = Files.readAllLines(Paths.get("stopwords.txt"));
        }
        catch(Exception e){
            throw new RuntimeException("Error in reading 'stopwords.txt'");
        }

        ta_label = new JLabel("Enter Some Text:");
        ta_label.setVerticalAlignment(JLabel.BOTTOM);


        textarea = new JTextArea();
        textarea.setPreferredSize(new Dimension(300, 300));
        textarea.setLineWrap(true);
        textarea.setWrapStyleWord(true);

        submit = new JButton("Find Stop words");
        submit.setSize(30, 10);
        
        out_label = new JLabel("List of Stop Words:");
        out_label.setVerticalAlignment(JLabel.BOTTOM);

        output = new JTextArea("No stopwords yet...");
        output.setEditable(false);
        output.setLineWrap(true);
        output.setWrapStyleWord(true);
        output.setPreferredSize(new Dimension(300, 300));

        setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.insets = new Insets(10, 10, 0, 0);
        gbc.anchor = GridBagConstraints.SOUTHWEST;
        add(ta_label, gbc);
        gbc.gridx = 1;
        gbc.gridy = 0;
        add(out_label, gbc);
        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.CENTER;
        add(textarea, gbc);
        gbc.gridx = 1;
        gbc.gridy = 1;
        add(output, gbc);
        gbc.gridx = 0;
        gbc.gridy = 2;
        add(submit, gbc);

        submit.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e){
                ArrayList<String> stopwords = findStopWords(textarea.getText());
                if(stopwords.isEmpty()) output.setText("No stopwords found!");
                else output.setText(String.join(" | ", stopwords));
                repaint();
            }
        });

        addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent windowEvent){
               System.exit(0);
            }
         });

        setTitle("Stop Words Finder");
        pack();
        setLocationRelativeTo(null);
        setVisible(true);
    }

    public ArrayList<String> findStopWords(String text){
        String words[] = text.toLowerCase().split("[ \n,;?.!'\"]");
        ArrayList<String> out = new ArrayList<String>();
        for(String word : words){
            if (!out.contains(word) && stopwords.contains(word)) out.add(word);
        }
        return out;
    }

    public static void main(String[] args) {
        new StopWordFinder();
    }
}