import com.robertopoletti.envprovider.EnvironmentProviderDescriptor;
import oasis.names.tc.xacml._3_0.core.schema.wd_17.AttributeDesignatorType;
import org.ow2.authzforce.core.pdp.api.AttributeProvider;
import org.ow2.authzforce.core.pdp.api.CloseableNamedAttributeProvider;
import org.ow2.authzforce.core.pdp.api.EnvironmentProperties;
import org.ow2.authzforce.core.pdp.api.value.AttributeValueFactoryRegistry;

import java.util.Set;

public class EnvironmentProviderFactory extends CloseableNamedAttributeProvider.FactoryBuilder<EnvironmentProviderDescriptor> {

    @Override
    public CloseableNamedAttributeProvider.DependencyAwareFactory getInstance(EnvironmentProviderDescriptor testAttributeProvider, EnvironmentProperties environmentProperties) throws IllegalArgumentException {
        return new CloseableNamedAttributeProvider.DependencyAwareFactory() {
            @Override
            public Set<AttributeDesignatorType> getDependencies() {
                return null;
            }

            @Override
            public CloseableNamedAttributeProvider getInstance(AttributeValueFactoryRegistry attributeValueFactoryRegistry, AttributeProvider attributeProvider) {
                return new EnvironmentProvider(attributeValueFactoryRegistry, attributeProvider);
            }
        };
    }

    @Override
    public Class<EnvironmentProviderDescriptor> getJaxbClass() {
        return EnvironmentProviderDescriptor.class;
    }
}