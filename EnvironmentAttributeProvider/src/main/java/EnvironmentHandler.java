import org.ow2.authzforce.core.pdp.api.EvaluationContext;
import org.ow2.authzforce.core.pdp.api.value.*;
import org.ow2.authzforce.xacml.identifiers.XacmlAttributeId;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class EnvironmentHandler  <AV extends AttributeValue>{
    private String attributeId;
    private Datatype<AV> datatype;

    public EnvironmentHandler(String attributeId, Datatype<AV> datatype) {
        this.attributeId = attributeId;
        this.datatype = datatype;
    }

    public AttributeBag<AV> retrieveAttribute(){
        switch(attributeId){
            case "urn:oasis:names:tc:xacml:1.0:environment:current-time":
                if(datatype.equals(StandardDatatypes.TIME)) {
                    DateTimeFormatter dtf = DateTimeFormatter.ISO_OFFSET_TIME;
                    ZonedDateTime currentTime = ZonedDateTime.now().truncatedTo(ChronoUnit.SECONDS);
                    AttributeBag<?> attributeBagResult = Bags.singletonAttributeBag(StandardDatatypes.TIME, new TimeValue(currentTime.format(dtf)));
                    return (AttributeBag<AV>) attributeBagResult;
                }
                break;
        }
        return null;
    }
}
